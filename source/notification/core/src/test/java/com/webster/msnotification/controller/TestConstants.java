package com.webster.msnotification.controller;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public final class TestConstants {
	/* Email addresses */
	public static final String NULL = null;
	public static final String EMPTY = "";
	public static final String VALID_EMAIL_ADDRESS = "Valid-Email@gmail.co.uk";
	public static final String INVALID_EMAIL_TOO_SHORT = "@b";
	public static final String INVALID_EMAIL_TOO_LONG = "Valid-Email".repeat(30)+"@gmail.co.uk";
	public static final String INVALID_EMAIL_NO_AT = "Invalid-Email-gmail.com";
	public static final String INVALID_EMAIL_HAS_WHITESPACE = "Invalid	@gmail.co.uk";
	public static final String INVALID_EMAIL_FORBIDDEN_CHARACTERS = "a\"b(c)d,e:f;g<h>i[j\\k]l@gmail.co.uk";
	public static final String VALID_TOKEN = "http://127.0.0.1:9900/Valid-token";
}
