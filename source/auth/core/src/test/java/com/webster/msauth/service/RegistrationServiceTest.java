package com.webster.msauth.service;

import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import java.util.Optional;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import com.webster.msauth.dto.RegisterUserDTO;
import com.webster.msauth.exception.UsernameAlreadyTakenException;
import com.webster.msauth.models.User;
import com.webster.msauth.repository.UserRepository;
import com.webster.msauth.service.RegistrationService;
import com.webster.msauth.service.UserDtoToEntityMapperService;

@ExtendWith(MockitoExtension.class)
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class RegistrationServiceTest {
	@Mock
	private UserRepository userRepository;
	@Mock
	private UserDtoToEntityMapperService userDtoToEntityMapperService;

	@InjectMocks
	private RegistrationService registrationService;

	@BeforeAll
	void setUp() {
		registrationService = new RegistrationService();
	}

	@Test
	void registerNotPossibleIfUsernameAlreadyTaken() {
		// Given
		User mockUser = Mockito.mock(User.class);
		RegisterUserDTO userDto = new RegisterUserDTO();
		given(userRepository.findByUsername(userDto.getUsername()))
				.willReturn(Optional.ofNullable(mockUser));

		// When & Then
		assertThatThrownBy(() -> registrationService.register(userDto))
				.isInstanceOf(UsernameAlreadyTakenException.class);
	}

	@Test
	void registerDoneIfUsernameDoesNotExist() {
		// Given
		RegisterUserDTO userDto = new RegisterUserDTO();
		given(userRepository.findByUsername(userDto.getUsername())).willReturn(Optional.ofNullable(null));

		// When
		registrationService.register(userDto);
		// Then
		verify(userDtoToEntityMapperService, times(1)).mapToUser(userDto);
		verify(userRepository, times(1)).save(any());
	}

}
