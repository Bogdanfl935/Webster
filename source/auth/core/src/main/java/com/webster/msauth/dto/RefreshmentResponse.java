package com.webster.msauth.dto;

import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@AllArgsConstructor
@Builder
public class RefreshmentResponse {
	@NotNull
	@Getter
	private String accessToken;
	@NotNull
	@Getter
	private String type;
	@NotNull
	@Getter
	private String subject;
	@NotNull
	@Getter
	private Long refreshTokenExpiration; /* In seconds */
}
