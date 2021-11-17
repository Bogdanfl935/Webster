package com.webster.msauth.dto;

import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public class AuthorizationResponse {
	@Getter
	@NotNull
	private Long accessTokenExpiration; /* In seconds */
}
