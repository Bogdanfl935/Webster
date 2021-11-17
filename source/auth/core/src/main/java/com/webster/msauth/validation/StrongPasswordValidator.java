package com.webster.msauth.validation;

import java.util.List;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

import org.passay.CharacterCharacteristicsRule;
import org.passay.CharacterRule;
import org.passay.EnglishCharacterData;
import org.passay.EnglishSequenceData;
import org.passay.IllegalSequenceRule;
import org.passay.LengthRule;
import org.passay.PasswordData;
import org.passay.PasswordValidator;
import org.passay.RuleResult;
import org.passay.WhitespaceRule;

import com.webster.msauth.constants.ValidationConstants;

public class StrongPasswordValidator implements ConstraintValidator<EnforcedStrongPassword, String> {
	@Override
	public void initialize(EnforcedStrongPassword constraintAnnotation) {

	}

	@Override
	public boolean isValid(String password, ConstraintValidatorContext context) {
		boolean isValidPassword = password != null;

		if (isValidPassword) {
			PasswordValidator validator = new PasswordValidator(List.of(
					new LengthRule(ValidationConstants.PASSWORD_MIN_LENGTH, ValidationConstants.PASSWORD_MAX_LENGTH),
					new CharacterCharacteristicsRule(3,
							List.of(new CharacterRule(EnglishCharacterData.UpperCase, 1),
									new CharacterRule(EnglishCharacterData.LowerCase, 1),
									new CharacterRule(EnglishCharacterData.Digit, 1),
									new CharacterRule(EnglishCharacterData.Special, 1))),
					new IllegalSequenceRule(EnglishSequenceData.Alphabetical, 5, false),
					new IllegalSequenceRule(EnglishSequenceData.Numerical, 5, false),
					new IllegalSequenceRule(EnglishSequenceData.USQwerty, 5, false), new WhitespaceRule()));

			RuleResult result = validator.validate(new PasswordData(password));

			if (!result.isValid()) {
				isValidPassword = false;
				String messageTemplate = String.join(" ", validator.getMessages(result));
				context.disableDefaultConstraintViolation();
				context.buildConstraintViolationWithTemplate(messageTemplate).addConstraintViolation();
			}
		} else {
			context.disableDefaultConstraintViolation();
			context.buildConstraintViolationWithTemplate("Field cannot be null").addConstraintViolation();
		}

		return isValidPassword;
	}
}
