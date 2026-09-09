from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer,UserSerializer
from .social import google,apple,facebook

from .serializers import FirebaseAuthSerializer
from .firebase import verify_firebase_token
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

from .serializers import CompleteRegistrationSerializer
from firebase_admin import auth

def tokens(u):
 r=RefreshToken.for_user(u); return {'access':str(r.access_token),'refresh':str(r),'user':UserSerializer(u).data}
class RegisterView(APIView):
 permission_classes=[AllowAny]
 def post(self,request):
  s=RegisterSerializer(data=request.data); s.is_valid(raise_exception=True); u=s.save(); return Response(tokens(u),status=201)
class LoginView(APIView):
 permission_classes=[AllowAny]
 def post(self,request):
  u=authenticate(username=request.data.get('username'),password=request.data.get('password'))
  if not u:return Response({'detail':'Invalid credentials'},status=401)
  return Response(tokens(u))
class MeView(APIView):
 def get(self,request):return Response(UserSerializer(request.user).data)
class GoogleView(APIView):
 permission_classes=[AllowAny]
 def post(self,r):return Response(tokens(google(r.data.get('id_token',''))))
class AppleView(APIView):
 permission_classes=[AllowAny]
 def post(self,r):return Response(tokens(apple(r.data.get('identity_token',''),r.data.get('email',''))))
class FacebookView(APIView):
 permission_classes=[AllowAny]
 def post(self,r):return Response(tokens(facebook(r.data.get('access_token',''))))
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .firebase import verify_firebase_token
from .serializers import FirebaseAuthSerializer


User = get_user_model()


class FirebaseAuthView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):

        # ---------------------------------------------------------
        # 1. Validate request
        # ---------------------------------------------------------

        serializer = FirebaseAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_token = serializer.validated_data["id_token"]
        device_token = serializer.validated_data.get("device_token")  # Extract device_token

        # ---------------------------------------------------------
        # 2. Verify Firebase ID token
        # ---------------------------------------------------------

        firebase_user = verify_firebase_token(id_token)

        if not firebase_user:
            return Response(
                {
                    "success": False,
                    "message": "Invalid Firebase ID token.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # ---------------------------------------------------------
        # 3. Extract Firebase information
        # ---------------------------------------------------------

        firebase_uid = firebase_user.get("uid")
        email = firebase_user.get("email")
        phone = firebase_user.get("phone_number")
        email_verified = firebase_user.get("email_verified", False)
        firebase_data = firebase_user.get("firebase", {})
        provider = firebase_data.get("sign_in_provider", "unknown")

        if email:
            email = email.strip().lower()

        # ---------------------------------------------------------
        # Safety check
        # ---------------------------------------------------------

        if not firebase_uid:
            return Response(
                {
                    "success": False,
                    "message": "Firebase UID is missing.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ---------------------------------------------------------
        # 4. FIRST: Find by Firebase UID
        # ---------------------------------------------------------

        user = User.objects.filter(firebase_uid=firebase_uid).first()
        is_new_user = False
        matched_by = None

        if user:
            matched_by = "firebase_uid"

        # ---------------------------------------------------------
        # 5. SECOND: Find by verified email
        # ---------------------------------------------------------

        if not user and email and email_verified:
            user = User.objects.filter(email__iexact=email).first()

            if user:
                matched_by = "email"

                if user.firebase_uid and user.firebase_uid != firebase_uid:
                    return Response(
                        {
                            "success": False,
                            "message": (
                                "An account already exists with this "
                                "email. Please use the existing login "
                                "method or link the accounts first."
                            ),
                            "code": "ACCOUNT_ALREADY_LINKED",
                        },
                        status=status.HTTP_409_CONFLICT,
                    )

                if not user.firebase_uid:
                    user.firebase_uid = firebase_uid

        # ---------------------------------------------------------
        # 6. CREATE NEW USER
        # ---------------------------------------------------------

        if not user:
            is_new_user = True

            if email:
                username = email
            elif phone:
                username = phone.replace("+", "")
            else:
                username = f"firebase_{firebase_uid[:12]}"

            original_username = username
            counter = 1

            while User.objects.filter(username=username).exists():
                username = f"{original_username}_{counter}"
                counter += 1

            user = User.objects.create_user(
                username=username,
                email=email or "",
                phone=phone or "",
                firebase_uid=firebase_uid,
                firebase_provider=provider,
                role="CUSTOMER",
                registration_completed=False,
                device_token=device_token,  # Saved on account creation
            )

            matched_by = "new_account"

        # ---------------------------------------------------------
        # 7. Update existing user information
        # ---------------------------------------------------------

        changed_fields = []

        if user.firebase_uid != firebase_uid:
            user.firebase_uid = firebase_uid
            changed_fields.append("firebase_uid")

        if user.firebase_provider != provider:
            user.firebase_provider = provider
            changed_fields.append("firebase_provider")

        if phone and not user.phone:
            user.phone = phone
            changed_fields.append("phone")

        if email and not user.email:
            user.email = email
            changed_fields.append("email")

        # Update device_token if provided and changed
        if device_token and user.device_token != device_token:
            user.device_token = device_token
            changed_fields.append("device_token")

        if changed_fields:
            user.save(update_fields=changed_fields)

        # ---------------------------------------------------------
        # 8. Generate Django JWT
        # ---------------------------------------------------------

        refresh = RefreshToken.for_user(user)

        # ---------------------------------------------------------
        # 9. Return response
        # ---------------------------------------------------------

        return Response(
            {
                "success": True,
                "is_new_user": is_new_user,
                "registration_completed": user.registration_completed,
                "requires_registration": not user.registration_completed,
                "matched_by": matched_by,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role,
                    "firebase_uid": user.firebase_uid,
                    "provider": user.firebase_provider,
                    "device_token": user.device_token,
                    "registration_completed": user.registration_completed,
                },
            },
            status=status.HTTP_200_OK,
        )
class CompleteRegistrationView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, request):

        user = request.user

        # Already completed
        if user.registration_completed:
            return Response(
                {
                    "success": False,
                    "message": "Registration is already completed.",
                    "registration_completed": True,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CompleteRegistrationSerializer(
            user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save(
            registration_completed=True
        )

        return Response(
            {
                "success": True,
                "message": "Registration completed successfully.",
                "registration_completed": True,

                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role,
                    "firebase_uid": user.firebase_uid,
                    "provider": user.firebase_provider,
                },
            },
            status=status.HTTP_200_OK,
        )        

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request):
        user = request.user

        firebase_uid = user.firebase_uid

        # Delete Firebase account first
        if firebase_uid:
            try:
                auth.delete_user(firebase_uid)
            except auth.UserNotFoundError:
                # Firebase user is already deleted
                pass
            except Exception as e:
                return Response(
                    {
                        "success": False,
                        "message": "Unable to delete Firebase account.",
                        "error": str(e),
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        # Delete Django user
        user.delete()

        return Response(
            {
                "success": True,
                "message": "Account deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )        