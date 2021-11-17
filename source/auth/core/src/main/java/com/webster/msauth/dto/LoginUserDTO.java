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
public class LoginUserDTO {
	@NotBlank
	@Size(max = ValidationConstants.EMAIL_MAX_LENGTH)
	@Getter
	@Setter
	private String username;

	@NotBlank
	@Size(max = ValidationConstants.PASSWORD_MAX_LENGTH)
	@Getter
	@Setter
	private String password;
}
