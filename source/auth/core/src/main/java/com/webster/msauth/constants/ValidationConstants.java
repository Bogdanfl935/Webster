package com.webster.msauth.constants;

import com.webster.msauth.token.OpaqueTokenHandle;

public final class ValidationConstants {
	/* User DTOs */
	public final static int EMAIL_MIN_LENGTH = 3;
	public final static int EMAIL_MAX_LENGTH = 254;
	public final static int PASSWORD_MIN_LENGTH = 8;
	public final static int PASSWORD_MAX_LENGTH = 30;
	/* Refresh Token DTO */
	public final static int REFRESH_TOKEN_MAX_LENGTH = 4 * OpaqueTokenHandle.OPAQUE_TOKEN_BYTE_LENGTH / 3 + 3;

	private ValidationConstants() {
	}
}
