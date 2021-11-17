package com.webster.msauth.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public class AuthenticationResponse {
	@Getter
	private String accessToken;
	@Getter
	private String refreshToken;
	@Getter
	private String type;
}
