package com.webster.msauth.service;

import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.webster.msauth.constants.JwtExpirationConstants;
import com.webster.msauth.dto.AccountNameDTO;
import com.webster.msauth.dto.ForgottenPasswordResponse;
import com.webster.msauth.exception.AuthExceptionMessage;
import com.webster.msauth.exception.InvalidUsernameException;
import com.webster.msauth.models.CustomUserDetails;
import com.webster.msauth.models.User;
import com.webster.msauth.repository.UserRepository;
import com.webster.msauth.token.JwtHandle;

@Service
public class ForgottenPasswordService {
	@Autowired
	private UserRepository userRepository;
	@Autowired
	private JwtHandle tokenHandle;

	public ForgottenPasswordResponse createResetToken(@Valid AccountNameDTO accountNameDTO) {
		Optional<User> locatedUser = userRepository.findByUsername(accountNameDTO.getUsername());

		if (locatedUser.isEmpty()) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.USERNAME_NOT_FOUND;
			exceptionMessage.setErrorParameter(accountNameDTO.getUsername());
			throw new InvalidUsernameException(exceptionMessage.getErrorMessage());
		}

		User user = locatedUser.get();

		String resetPassToken = tokenHandle.createJsonWebToken(new CustomUserDetails(user),
				JwtExpirationConstants.RESET_PASSWORD_TOKEN_EXPIRATION_MILLISEC);
		return new ForgottenPasswordResponse(resetPassToken);
	}

}
