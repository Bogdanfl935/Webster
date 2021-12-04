package com.webster.msauth.service;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.webster.msauth.exception.AccountAlreadyConfirmedException;
import com.webster.msauth.exception.AuthExceptionMessage;
import com.webster.msauth.exception.InvalidUsernameException;
import com.webster.msauth.models.User;
import com.webster.msauth.repository.UserRepository;
import com.webster.msauth.token.JwtHandle;
import com.webster.msauth.token.JwtScopeClaim;
import com.webster.msauth.token.JwtValidator;

@Service
public class ConfirmationService {
	@Autowired
	private JwtHandle tokenHandle;
	@Autowired
	private JwtValidator tokenValidator;
	@Autowired
	private UserRepository userRepository;

	public void confirm(String rawToken) {
		String token = tokenValidator.stripTokenPrefix(rawToken);
		/* If token is invalid, an exception will be thrown */
		tokenValidator.validate(token, JwtScopeClaim.CONFIRM);

		String username = tokenHandle.getJwtSubject(token);
		Optional<User> locatedUser = userRepository.findByUsername(username);

		/*
		 * Check whether there is an user with that particular username (May have been
		 * deleted after confirmation had been sent out)
		 */
		if (locatedUser.isEmpty()) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.USERNAME_NOT_FOUND;
			throw new InvalidUsernameException(exceptionMessage.getErrorMessage());
		}

		User user = locatedUser.get();

		/*
		 * Check whether the user had already used the token to activate their account
		 */
		if (user.isCredentialsNonExpired()) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.ACCOUNT_ALREADY_CONFIRMED;
			throw new AccountAlreadyConfirmedException(exceptionMessage.getErrorMessage());
		}
		
		user.setCredentialsNonExpired(true);
		userRepository.save(user);
	}

}
