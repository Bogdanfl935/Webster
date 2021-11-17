package com.webster.msnotification.constants;

public class ExternConfigConstants {
	/* Mail session constants */
	public static final String MAIL_SESSION_HOST = "${motorage.msnotification.mail-session-host}";
	public static final String MAIL_SESSION_PORT = "${motorage.msnotification.mail-session-port}";
	public static final String MAIL_SESSION_USERNAME = "${motorage.msnotification.mail-session-username}";
	public static final String MAIL_SESSION_PASSWORD = "${motorage.msnotification.mail-session-password}";
	
	/* Foreign endpoints */
	public static final String ACCOUNT_CONFIRMATION_TARGET = "${motorage.msnotification.account-confirmation.url}";
	public static final String PASSWORD_RESET_TARGET = "${motorage.msnotification.password-reset.url}";
}
