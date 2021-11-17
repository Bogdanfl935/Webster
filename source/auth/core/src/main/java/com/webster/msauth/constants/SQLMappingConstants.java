package com.webster.msauth.constants;

public final class SQLMappingConstants {
	private static final String SEPARATOR = "_";
	private static final String IDENTIFIER = "id";

	/* Primary table constants */
	public static final String USER = "App_User";
	public static final String UNCONFIRMED_USER = "Unconfirmed_User";
	public static final String ROLE = "Role";

	/* Joint table constants */
	public static final String USER_JOINT_ROLE = USER + SEPARATOR + ROLE;

	/* Foreign key constants */
	public static final String USER_FOREIGN_KEY = USER + SEPARATOR + IDENTIFIER;
	public static final String ROLE_FOREIGN_KEY = ROLE + SEPARATOR + IDENTIFIER;

	private SQLMappingConstants() {
	}
}
