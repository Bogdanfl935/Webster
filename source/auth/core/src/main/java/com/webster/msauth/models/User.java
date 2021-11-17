package com.webster.msauth.models;

import java.util.List;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.Table;

import com.webster.msauth.constants.SQLMappingConstants;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

@Entity
@Table(name = SQLMappingConstants.USER)
@RequiredArgsConstructor
@NoArgsConstructor
public class User {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;

	@Getter
	@Setter
	@NonNull
	private String username;
	@Getter
	@Setter
	@NonNull
	private String password;
	@Getter
	@Setter
	private boolean isEnabled;
	@Getter
	@Setter
	private boolean isCredentialsNonExpired;

	@ManyToMany
	@JoinTable(name = SQLMappingConstants.USER_JOINT_ROLE, joinColumns = @JoinColumn(name = SQLMappingConstants.USER_FOREIGN_KEY), inverseJoinColumns = @JoinColumn(name = SQLMappingConstants.ROLE_FOREIGN_KEY))
	@Getter
	private List<Role> roles;
}
