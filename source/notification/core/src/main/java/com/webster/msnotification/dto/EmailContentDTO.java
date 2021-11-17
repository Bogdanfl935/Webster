package com.webster.msnotification.dto;

import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

@AllArgsConstructor
@Builder
public class EmailContentDTO {
	@Getter
	@NotNull
	private String destination;
	@Getter
	@NotNull
	private String subject;
	@Getter
	@NotNull
	private String content;
}
