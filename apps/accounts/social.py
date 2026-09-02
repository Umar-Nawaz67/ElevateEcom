import requests,jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from .models import User,SocialAccount

def user_for(provider,pid,email='',name=''):
 s=SocialAccount.objects.select_related('user').filter(provider=provider,provider_user_id=pid).first()
 if s:return s.user
 email=(email or '').strip().lower(); u=User.objects.filter(email__iexact=email).first() if email else None
 if not u:
  base=(email.split('@')[0] if email else f'{provider}_{pid}')[:120]; username=base
  if User.objects.filter(username=username).exists(): username=f'{base}_{pid[:12]}'[:150]
  u=User.objects.create_user(username=username,email=email,first_name=(name.split()[0] if name else ''))
 SocialAccount.objects.create(user=u,provider=provider,provider_user_id=pid,email=email); return u

def google(token):
 if not settings.GOOGLE_WEB_CLIENT_ID: raise AuthenticationFailed('GOOGLE_WEB_CLIENT_ID is not configured')
 try: info=id_token.verify_oauth2_token(token,google_requests.Request(),settings.GOOGLE_WEB_CLIENT_ID)
 except Exception as e: raise AuthenticationFailed(f'Invalid Google ID token: {e}')
 return user_for('google',info['sub'],info.get('email',''),info.get('name',''))

def facebook(token):
 if not settings.FACEBOOK_APP_ID or not settings.FACEBOOK_APP_SECRET: raise AuthenticationFailed('Facebook credentials are not configured')
 app=f'{settings.FACEBOOK_APP_ID}|{settings.FACEBOOK_APP_SECRET}'
 d=requests.get('https://graph.facebook.com/debug_token',params={'input_token':token,'access_token':app},timeout=10).json().get('data',{})
 if not d.get('is_valid') or str(d.get('app_id'))!=str(settings.FACEBOOK_APP_ID): raise AuthenticationFailed('Invalid Facebook token')
 p=requests.get('https://graph.facebook.com/me',params={'fields':'id,name,email','access_token':token},timeout=10).json()
 return user_for('facebook',p['id'],p.get('email',''),p.get('name',''))

def apple(token,email=''):
 try:
  kid=jwt.get_unverified_header(token)['kid']; keys=requests.get('https://appleid.apple.com/auth/keys',timeout=10).json()['keys']; key=next(k for k in keys if k['kid']==kid)
  c=jwt.decode(token,key,algorithms=['RS256'],audience=settings.APPLE_CLIENT_ID or None,issuer='https://appleid.apple.com')
 except Exception as e: raise AuthenticationFailed(f'Invalid Apple identity token: {e}')
 return user_for('apple',c['sub'],c.get('email') or email,'')
