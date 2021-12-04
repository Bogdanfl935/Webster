package com.webster.msauth.dto;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

import com.webster.msauth.constants.ValidationConstants;
import com.webster.msauth.validation.EnforcedStrongPassword;
import com.webster.msauth.validation.PasswordMatch;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@PasswordMatch
@NoArgsConstructor
@AllArgsConstructor
public class RegisterUserDTO implements PasswordCarrierDTO{
	@NotBlank
	@Email
	@Size(max = ValidationConstants.EMAIL_MAX_LENGTH)
	@Getter
	@Setter
	private String username;

	
	@EnforcedStrongPassword
	@NotNull
	@Getter
	@Setter
	private String password;

	@NotNull
	@Getter
	@Setter
	private String confirmPassword;
}
