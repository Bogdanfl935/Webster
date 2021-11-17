package com.webster.msauth.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public class ConfirmationTokenResponse {
	@Getter
	private String confirmationToken;
}
