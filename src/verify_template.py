# src/utils/email_templates.py

def verify_email_template(link: str, user_name: str = "Customer") -> str:
    """
    Returns a professional HTML email template for email verification.
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Verify Your Email</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f7; margin:0; padding:0;">
        <table width="100%" bgcolor="#f4f4f7" cellpadding="0" cellspacing="0">
            <tr>
                <td align="center">
                    <table width="600" bgcolor="#ffffff" cellpadding="20" cellspacing="0" style="border-radius: 8px; margin-top: 40px; margin-bottom: 40px;">
                        <tr>
                            <td align="center">
                                <img src="https://yourdomain.com/logo.png" alt="App Logo" width="120" style="margin-bottom: 20px;">
                            </td>
                        </tr>
                        <tr>
                            <td align="center" style="font-size: 24px; font-weight: bold; color: #333333;">
                                Verify Your Email Address
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size: 16px; color: #555555; line-height: 1.5;">
                                Hello {user_name},<br><br>
                                Thank you for signing up! Please click the button below to verify your email address and activate your account.
                            </td>
                        </tr>
                        <tr>
                            <td align="center">
                                <a href="{link}" style="background-color: #28a745; color: #ffffff; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                                    Verify Email
                                </a>
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size: 12px; color: #999999; text-align: center; padding-top: 20px;">
                                If the button doesn't work, copy and paste this link into your browser:<br>
                                <a href="{link}" style="color: #28a745;">{link}</a>
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size: 12px; color: #999999; text-align: center;">
                                © 2026 Your App Name. All rights reserved.
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def reset_password_template(link: str, user_name: str = "User") -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Reset Your Password</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f7; margin:0; padding:0;">
        <table width="100%" bgcolor="#f4f4f7" cellpadding="0" cellspacing="0">
            <tr>
                <td align="center">
                    <table width="600" bgcolor="#ffffff" cellpadding="20" cellspacing="0" style="border-radius: 8px; margin: 40px auto;">
                       
                        <tr>
                            <td align="center" style="font-size: 24px; font-weight: bold; color: #333;">
                                Reset Your Password
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size: 16px; color: #555; line-height: 1.5;">
                                Hello {user_name},<br><br>
                                We received a request to reset your password. Click the button below to set a new password.
                                If you did not request this change, you can safely ignore this email.
                            </td>
                        </tr>
                        <tr>
                            <td align="center">
                                <a href="{link}" style="background-color: #007BFF; color: #fff; padding: 12px 25px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                                    Reset Password
                                </a>
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size: 12px; color: #999; text-align: center; padding-top: 20px;">
                                If the button doesn't work, copy and paste this link into your browser:<br>
                                <a href="{link}" style="color: #007BFF;">{link}</a>
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size: 12px; color: #999; text-align: center;">
                                © 2026 Your App Name. All rights reserved.
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
