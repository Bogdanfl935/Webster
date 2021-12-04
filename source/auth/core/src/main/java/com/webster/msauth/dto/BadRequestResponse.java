package com.webster.msauth.dto;

import java.util.Date;
import java.util.List;

import javax.validation.constraints.NotNull;

import lombok.Builder;
import lombok.Getter;

@Builder
public class BadRequestResponse {
	@NotNull
	@Getter
	final private Date timestamp = new Date();
	@NotNull
	@Getter
	private Integer status;
	@NotNull
	@Getter
	private String error;
	@NotNull
	@Getter
	private List<ErrorDetailsDTO> errors;
}
