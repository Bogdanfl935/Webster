package com.webster.msauth.models;

import javax.persistence.Entity;
import javax.persistence.Id;

import org.springframework.data.redis.core.RedisHash;
import org.springframework.data.redis.core.TimeToLive;

import com.webster.msauth.constants.JedisConstants;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

@Entity
@RequiredArgsConstructor
@NoArgsConstructor
@RedisHash(timeToLive=JedisConstants.ENTITY_TTL_SECONDS)
public class RefreshToken {
	@Id
	@NonNull
	@Getter
	@Setter
	private String id;
	@NonNull
	@Getter
	@Setter
	private String username;
	@TimeToLive
	@Getter
	@Setter
	private Long timeout;
}
