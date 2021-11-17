package com.webster.msnotification.constants;

public class ExternConfigConstants {
	/* Mail session constants */
	public static final String MAIL_SESSION_HOST = "${webster.msnotification.mail-session-host}";
	public static final String MAIL_SESSION_PORT = "${webster.msnotification.mail-session-port}";
	public static final String MAIL_SESSION_USERNAME = "${webster.msnotification.mail-session-username}";
	public static final String MAIL_SESSION_PASSWORD = "${webster.msnotification.mail-session-password}";
	
	/* Foreign endpoints */
	public static final String ACCOUNT_CONFIRMATION_TARGET = "${webster.msnotification.account-confirmation.url}";
	public static final String PASSWORD_RESET_TARGET = "${webster.msnotification.password-reset.url}";
}
