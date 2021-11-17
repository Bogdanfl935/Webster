package com.webster.msauth.token;

import java.security.SecureRandom;
import java.util.Base64;

import org.springframework.stereotype.Component;

@Component
public class OpaqueTokenHandle {
	public static final int OPAQUE_TOKEN_BYTE_LENGTH = 64;
	
	public String createRefreshToken() {
		SecureRandom randomSecurer = new SecureRandom();
		byte[] byteArray = new byte[OPAQUE_TOKEN_BYTE_LENGTH];
		randomSecurer.nextBytes(byteArray);
		return Base64.getEncoder().encodeToString(byteArray);
	}
}
