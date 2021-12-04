package com.webster.msauth.dto;

import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
public class ErrorDetailsDTO {
	@Getter
	@NotNull
	private String fieldName;
	@Getter
	@NotNull
	private String errorMessage;
}
