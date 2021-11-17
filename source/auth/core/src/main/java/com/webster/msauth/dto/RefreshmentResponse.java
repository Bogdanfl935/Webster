package com.webster.msauth.dto;

import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public class RefreshmentResponse {
	@NotNull
	@Getter
	private String accessToken;
	@NotNull
	@Getter
	private Long refreshTokenExpiration; /* In seconds */
}
