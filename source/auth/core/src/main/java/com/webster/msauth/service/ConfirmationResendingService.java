package com.webster.msauth.service;

import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.webster.msauth.constants.JwtExpirationConstants;
import com.webster.msauth.dto.AccountNameDTO;
import com.webster.msauth.dto.ConfirmationTokenResponse;
import com.webster.msauth.exception.AccountAlreadyConfirmedException;
import com.webster.msauth.exception.AuthExceptionMessage;
import com.webster.msauth.exception.InvalidUsernameException;
import com.webster.msauth.models.CustomUserDetails;
import com.webster.msauth.models.User;
import com.webster.msauth.repository.UserRepository;
import com.webster.msauth.token.JwtHandle;

@Service
public class ConfirmationResendingService {
	@Autowired
	private UserRepository userRepository;
	@Autowired
	private JwtHandle tokenHandle;

	public ConfirmationTokenResponse resend(@Valid AccountNameDTO accountNameDTO) {
		Optional<User> locatedUser = userRepository.findByUsername(accountNameDTO.getUsername());

		if (locatedUser.isEmpty()) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.USERNAME_NOT_FOUND;
			exceptionMessage.setErrorParameter(accountNameDTO.getUsername());
			throw new InvalidUsernameException(exceptionMessage.getErrorMessage());
		}

		User user = locatedUser.get();

		if (user.isEnabled()) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.ACCOUNT_ALREADY_CONFIRMED;
			exceptionMessage.setErrorParameter(accountNameDTO.getUsername());
			throw new AccountAlreadyConfirmedException(exceptionMessage.getErrorMessage());
		}

		String confirmationToken = tokenHandle.createJsonWebToken(new CustomUserDetails(user),
				JwtExpirationConstants.EMAIL_CONFIRMATION_TOKEN_EXPIRATION_MILLISEC);
		return new ConfirmationTokenResponse(confirmationToken);
	}
}
