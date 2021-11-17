package com.webster.msauth.controller;

public final class TestConstants {
	/* Email addresses */
	public static final String VALID_EMAIL_ADDRESS = "Valid-Email@gmail.co.uk";
	public static final String INVALID_EMAIL_TOO_SHORT = "@b";
	public static final String INVALID_EMAIL_TOO_LONG = "Valid-Email".repeat(30)+"@gmail.co.uk";
	public static final String INVALID_EMAIL_NO_AT = "Invalid-Email-gmail.com";
	public static final String INVALID_EMAIL_HAS_WHITESPACE = "Invalid	@gmail.co.uk";
	public static final String INVALID_EMAIL_FORBIDDEN_CHARACTERS = "a\"b(c)d,e:f;g<h>i[j\\k]l@gmail.co.uk";
	
	/* Passwords */
	public static final String VALID_PASSWORD_ONE = "123unencryptedPassword";
	public static final String VALID_PASSWORD_TWO = "@unencryptedPassword";
	public static final String INVALID_PASSWORD_TOO_SHORT = "@uP";
	public static final String INVALID_PASSWORD_TOO_LONG = "@uP".repeat(15);
	public static final String INVALID_PASSWORD_HAS_WHITESPACE = "@	unencryptedPassword";
	public static final String INVALID_PASSWORD_HAS_ALPHABET_SEQUENCE = "@abcdefghijkl55";
	public static final String INVALID_PASSWORD_HAS_NUMERIC_SEQUENCE = "@012345678password";
	public static final String INVALID_PASSWORD_HAS_QWERTY_SEQUENCE = "@asdfghjkl@@";
	public static final String INVALID_ONE_CHARACTER_CONSTRAINT = "password";
	public static final String INVALID_TWO_CHARACTERS_CONSTRAINT = "@password";
	
	private TestConstants() {
	}
}
