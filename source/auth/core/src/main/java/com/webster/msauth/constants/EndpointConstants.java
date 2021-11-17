package com.webster.msauth.constants;

public final class EndpointConstants {
	/* URI constants */
	/* Mandatory endpoints */
	public static final String REGISTRATION = "/registration";
	public static final String AUTHENTICATION = "/authentication";
	public static final String AUTHORIZATION = "/authorization";
	public static final String REFRESHMENT = "/refreshment";
	public static final String CONFIRMATION = "/confirmation";
	/* Optional endpoints */
	public static final String CONFIRMATION_RESENDING = "/confirmation-resending";
	public static final String PASSWORD_RESETTING = "/password-resetting";
	public static final String PASSWORD_FORGOTTEN = "/password-forgotten";

	/* Header constants */
	public static final String AUTHORIZATION_HEADER = "Authorization";

	private EndpointConstants() {
	}
}
