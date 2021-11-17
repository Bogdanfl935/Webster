package com.webster.msauth.dto;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

import com.webster.msauth.constants.ValidationConstants;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@AllArgsConstructor
@NoArgsConstructor
public class RefreshTokenDTO {
	@Getter
	@Setter
	@NotBlank
	@Size(max = ValidationConstants.REFRESH_TOKEN_MAX_LENGTH)
	private String refreshToken;
}
