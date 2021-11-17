package com.webster.msauth.dto;

import javax.validation.constraints.NotNull;

import com.webster.msauth.validation.EnforcedStrongPassword;
import com.webster.msauth.validation.PasswordMatch;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@PasswordMatch
@NoArgsConstructor
@AllArgsConstructor
public class PasswordResetDTO implements PasswordCarrierDTO{
	@EnforcedStrongPassword
	@Getter
	@Setter
	private String password;

	@NotNull
	@Getter
	@Setter
	private String confirmPassword;
}
