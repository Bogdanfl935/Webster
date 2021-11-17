package com.webster.msauth.service;

import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.webster.msauth.dto.PasswordResetDTO;
import com.webster.msauth.exception.AuthExceptionMessage;
import com.webster.msauth.exception.InvalidAccessTokenProvidedException;
import com.webster.msauth.models.User;
import com.webster.msauth.repository.UserRepository;
import com.webster.msauth.token.JwtHandle;
import com.webster.msauth.token.JwtValidator;

@Service
public class PasswordResetService {
	@Autowired
	private JwtHandle tokenHandle;
	@Autowired
	private JwtValidator tokenValidator;
	@Autowired
	private UserRepository userRepository;
	@Autowired
	private PasswordEncoder passwordEncoder;

	public void reset(@Valid PasswordResetDTO passwordResetDTO, String rawToken) {
		String token = tokenValidator.stripTokenPrefix(rawToken);
		/* If token is invalid, an exception will be thrown */
		tokenValidator.validate(token);

		String username = tokenHandle.getJwtSubject(token);
		Optional<User> locatedUser = userRepository.findByUsername(username);

		/*
		 * Check whether there is an user with that particular username (May have been
		 * deleted after confirmation had been sent out)
		 */
		if (locatedUser.isEmpty()) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.INVALID_ACCESS_TOKEN_PROVIDED;
			throw new InvalidAccessTokenProvidedException(exceptionMessage.getErrorMessage());
		}

		User user = locatedUser.get();

		/*
		 * Check whether the user had already used the token to reset their password
		 */
		if (user.isCredentialsNonExpired()) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.INVALID_ACCESS_TOKEN_PROVIDED;
			throw new InvalidAccessTokenProvidedException(exceptionMessage.getErrorMessage());
		}

		user.setCredentialsNonExpired(true);
		user.setPassword(passwordEncoder.encode(passwordResetDTO.getPassword()));
		userRepository.save(user);
	}

}