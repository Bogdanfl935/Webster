package com.webster.msauth.service;

import javax.validation.Valid;

import org.modelmapper.Converter;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.webster.msauth.dto.RegisterUserDTO;
import com.webster.msauth.models.User;

@Service
public class UserDtoToEntityMapperService {
	@Autowired
	private PasswordEncoder passwordEncoder;
	
	public User mapToUser(@Valid RegisterUserDTO registerUserDto) {
		ModelMapper modelMapper = new ModelMapper();
		Converter<String, String> toEncodedPassword = ctx -> ctx.getSource() == null ? null
				: passwordEncoder.encode(ctx.getSource());

		modelMapper.typeMap(RegisterUserDTO.class, User.class).addMappings(
				mapper -> mapper.using(toEncodedPassword).map(RegisterUserDTO::getPassword, User::setPassword));

		return modelMapper.map(registerUserDto, User.class);
	}
}
