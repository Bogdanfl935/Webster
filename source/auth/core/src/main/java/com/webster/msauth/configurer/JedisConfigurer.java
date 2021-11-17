package com.webster.msauth.configurer;

import java.time.Duration;

import javax.validation.constraints.NotNull;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisPassword;
import org.springframework.data.redis.connection.RedisStandaloneConfiguration;
import org.springframework.data.redis.connection.jedis.JedisClientConfiguration;
import org.springframework.data.redis.connection.jedis.JedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;

import com.webster.msauth.constants.ExternConfigConstants;

import lombok.Getter;

@Configuration
public class JedisConfigurer {
	@Value(ExternConfigConstants.JEDIS_CONFIG_HOST)
	@Getter
	@NotNull
	private String host;
	@Getter
	@NotNull
	@Value(ExternConfigConstants.JEDIS_CONFIG_PORT)
	private Integer port;
	@Getter
	@NotNull
	@Value(ExternConfigConstants.JEDIS_CONFIG_DATABASE)
	private Integer database;
	@Getter
	@NotNull
	@Value(ExternConfigConstants.JEDIS_CONFIG_PASSWORD)
	private String password;
	

	@Bean
	JedisConnectionFactory getJedisConnectionFactory() {
		RedisStandaloneConfiguration redisStandaloneConfiguration = new RedisStandaloneConfiguration(host, port);
		redisStandaloneConfiguration.setDatabase(database);
		redisStandaloneConfiguration.setPassword(RedisPassword.of(password));

		JedisClientConfiguration jedisClientConfiguration = JedisClientConfiguration.builder()
				.connectTimeout(Duration.ofSeconds(60)).build();

		return new JedisConnectionFactory(redisStandaloneConfiguration, jedisClientConfiguration);
	}

	@Bean
	public RedisTemplate<String, Object> getRedisTemplate() {
		RedisTemplate<String, Object> redisTemplate = new RedisTemplate<>();
		redisTemplate.setConnectionFactory(getJedisConnectionFactory());
		return redisTemplate;
	}
}
