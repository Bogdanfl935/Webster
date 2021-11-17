package com.webster.msauth.constants;

public final class ExternConfigConstants {
	/* Token configuration */
	public static final String TOKEN_CONFIG_JWT_ISSUER = "${motorage.msauth.token-config.jwt-issuer}";
	
	/* Redis configuration */
	public static final String JEDIS_CONFIG_HOST = "${motorage.msauth.jedis-config.host}";
	public static final String JEDIS_CONFIG_PORT ="${motorage.msauth.jedis-config.port}";
	public static final String JEDIS_CONFIG_DATABASE ="${motorage.msauth.jedis-config.database}";
	public static final String JEDIS_CONFIG_PASSWORD ="${motorage.msauth.jedis-config.password}";

	private ExternConfigConstants() {
	}
}
