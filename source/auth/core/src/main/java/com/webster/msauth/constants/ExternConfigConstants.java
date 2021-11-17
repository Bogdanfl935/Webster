package com.webster.msauth.constants;

public final class ExternConfigConstants {
	/* Token configuration */
	public static final String TOKEN_CONFIG_JWT_ISSUER = "${webster.msauth.token-config.jwt-issuer}";
	
	/* Redis configuration */
	public static final String JEDIS_CONFIG_HOST = "${webster.msauth.jedis-config.host}";
	public static final String JEDIS_CONFIG_PORT ="${webster.msauth.jedis-config.port}";
	public static final String JEDIS_CONFIG_DATABASE ="${webster.msauth.jedis-config.database}";
	public static final String JEDIS_CONFIG_PASSWORD ="${webster.msauth.jedis-config.password}";

	private ExternConfigConstants() {
	}
}
