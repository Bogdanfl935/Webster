package com.webster.msauth.service;

import java.util.Optional;

import javax.validation.Valid;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.webster.msauth.constants.JwtExpirationConstants;
import com.webster.msauth.dto.ConfirmationTokenResponse;
import com.webster.msauth.dto.RegisterUserDTO;
import com.webster.msauth.exception.AuthExceptionMessage;
import com.webster.msauth.exception.UsernameAlreadyTakenException;
import com.webster.msauth.models.CustomUserDetails;
import com.webster.msauth.models.User;
import com.webster.msauth.repository.UserRepository;
import com.webster.msauth.token.JwtHandle;

@Service
public class RegistrationService {
	@Autowired
	private UserRepository userRepository;
	@Autowired
	private UserDtoToEntityMapperService userDtoToEntityMapperService;
	@Autowired
	private JwtHandle tokenHandle;

	public ConfirmationTokenResponse register(@Valid RegisterUserDTO registerUserDTO) {
		Optional<User> locatedUser = userRepository.findByUsername(registerUserDTO.getUsername());

		if (locatedUser.isPresent()) {
			AuthExceptionMessage exceptionMessage = AuthExceptionMessage.USERNAME_ALREADY_TAKEN;
			exceptionMessage.setErrorParameter(registerUserDTO.getUsername());
			throw new UsernameAlreadyTakenException(exceptionMessage.getErrorMessage());
		}

		User unconfirmedUser = userDtoToEntityMapperService.mapToUser(registerUserDTO);
		unconfirmedUser.setCredentialsNonExpired(true);
		unconfirmedUser.setEnabled(false);
		userRepository.save(unconfirmedUser);
		
		String confirmationToken = tokenHandle.createJsonWebToken(new CustomUserDetails(unconfirmedUser),
				JwtExpirationConstants.EMAIL_CONFIRMATION_TOKEN_EXPIRATION_MILLISEC);
		return new ConfirmationTokenResponse(confirmationToken);
	}

}
