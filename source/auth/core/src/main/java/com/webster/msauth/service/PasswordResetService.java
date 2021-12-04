package com.webster.msauth.service;

import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.webster.msauth.dto.PasswordResetDTO;
import com.webster.msauth.exception.AuthExceptionMessage;
import com.webster.msauth.exception.InvalidUsernameException;
import com.webster.msauth.models.User;
import com.webster.msauth.repository.UserRepository;
import com.webster.msauth.token.JwtHandle;
import com.webster.msauth.token.JwtScopeClaim;
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
		tokenValidator.validate(token, JwtScopeClaim.RESET);

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

		user.setPassword(passwordEncoder.encode(passwordResetDTO.getPassword()));
		userRepository.save(user);
	}

}
