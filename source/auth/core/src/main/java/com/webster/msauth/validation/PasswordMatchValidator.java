package com.webster.msauth.validation;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

import com.webster.msauth.constants.ValidationConstants;
import com.webster.msauth.dto.PasswordCarrierDTO;

public class PasswordMatchValidator implements ConstraintValidator<PasswordMatch, PasswordCarrierDTO> {
	private String message;

	@Override
	public void initialize(PasswordMatch constraintAnnotation) {
		message = ValidationConstants.CUSTOM_CONSTRAINT_PREFIX + constraintAnnotation.message();
	}

	@Override
	public boolean isValid(PasswordCarrierDTO passwordDto, ConstraintValidatorContext context) {
		boolean isMatch = passwordDto.getPassword() != null && passwordDto.getPassword().equals(passwordDto.getConfirmPassword());

		if (!isMatch) {
			context.disableDefaultConstraintViolation();
			context.buildConstraintViolationWithTemplate(message).addPropertyNode("confirmPassword").addConstraintViolation();
		}

		return isMatch;
	}
}
