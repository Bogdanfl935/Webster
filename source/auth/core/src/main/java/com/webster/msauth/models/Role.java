package com.webster.msauth.models;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import com.webster.msauth.constants.SQLMappingConstants;

import lombok.Getter;

@Entity
@Table(name=SQLMappingConstants.ROLE)
public class Role {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;
	
	@Getter
	private String title;
}
