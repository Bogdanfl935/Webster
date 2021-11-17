package com.webster.msauth.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public class ForgottenPasswordResponse {
	@Getter
	private String passwordResetToken;
}
