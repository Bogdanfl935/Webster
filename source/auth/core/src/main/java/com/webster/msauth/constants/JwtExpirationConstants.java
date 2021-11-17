package com.webster.msauth.constants;

public final class JwtExpirationConstants {
	/* Time constants */
	public static final Long MINUTE_TO_MILLISEC = 60 * 1000L;

	public static final Long GENERAL_ACCESS_TOKEN_EXPIRATION_MILLISEC = 5 * MINUTE_TO_MILLISEC; /* 5 minutes */
	public static final Long EMAIL_CONFIRMATION_TOKEN_EXPIRATION_MILLISEC = 1440 * MINUTE_TO_MILLISEC; /* 1 day */
	public static final Long RESET_PASSWORD_TOKEN_EXPIRATION_MILLISEC = 60 * MINUTE_TO_MILLISEC; /* 1 hour */

	private JwtExpirationConstants() {

	}
}
