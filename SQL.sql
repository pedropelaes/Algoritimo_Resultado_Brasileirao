CREATE TABLE TECNICOS(
	id_tecnico SERIAL CONSTRAINT pk_tecnico PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	status VARCHAR(10) NOT NULL,
	media_pontos NUMERIC(2,2)
);

CREATE TABLE TIMES(
	id_time SERIAL NOT NULL CONSTRAINT pk_time PRIMARY KEY,
	id_tecnico INTEGER,
	nome VARCHAR(80) NOT NULL,
	posicao VARCHAR(3) NOT NULL,
	vitorias INTEGER,
	empates INTEGER, 
	derrotas INTEGER,
	nota NUMERIC(2, 2),
	CONSTRAINT fk_tecnico FOREIGN KEY (id_tecnico) REFERENCES TECNICOS(id_tecnico)
);

CREATE TABLE JOGADORES(
	id_jogador SERIAL CONSTRAINT pk_jogador PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	id_time INTEGER,
	posicao VARCHAR(20) NOT NULL,
	status VARCHAR(10) NOT NULL,
	amarelos INTEGER,
	vermelhos INTEGER,
	nota NUMERIC(2, 2),
	CONSTRAINT fk_time FOREIGN KEY (id_time) REFERENCES TIMES(id_time)
);

CREATE TABLE ARBITROS(
	id_arbitro SERIAL CONSTRAINT pk_arbitro PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	media_amarelos NUMERIC(2,2),
	media_vermelhos NUMERIC(2,2)
);

CREATE TABLE PARTIDA(
	id_partida SERIAL CONSTRAINT pk_partida PRIMARY KEY,
	id_mandante INTEGER NOT NULL,
	id_visitante INTEGER NOT NULL,
	escalacao_mandante INTEGER NOT NULL,
	escalacao_visitante INTEGER NOT NULL,
	id_arbitro INTEGER NOT NULL,
	data DATE NOT NULL,
	CONSTRAINT fk_mandante FOREIGN KEY (id_mandante) REFERENCES TIMES(id_time),
	CONSTRAINT fk_visitante FOREIGN KEY (id_visitante) REFERENCES TIMES(id_time),
	CONSTRAINT fk_arbitro FOREIGN KEY (id_arbitro) REFERENCES ARBITROS(id_arbitro)
);

CREATE TABLE ESCALACAO(
	id_escalacao SERIAL CONSTRAINT pk_escalacao PRIMARY KEY,
	id_partida INTEGER NOT NULL,
	CONSTRAINT fk_partida FOREIGN KEY (id_partida) REFERENCES PARTIDA(id_partida)
);

CREATE TABLE JOGADOR_ESCALACAO(
	id_escalacao INTEGER NOT NULL,
	id_jogador INTEGER NOT NULL,
	CONSTRAINT fk_escalacao FOREIGN KEY (id_escalacao) REFERENCES ESCALACAO(id_escalacao),
	CONSTRAINT fk_jogador FOREIGN KEY (id_jogador) REFERENCES JOGADORES(id_jogador),
	CONSTRAINT pk_jog_esc PRIMARY KEY (id_escalacao, id_jogador)
);

ALTER TABLE PARTIDA
	ADD CONSTRAINT fk_esc_mandante FOREIGN KEY (escalacao_mandante) REFERENCES ESCALACAO(id_escalacao)
	ADD CONSTRAINT fk_esc_visitante FOREIGN KEY (escalacao_visitante) REFERENCES ESCALACAO(id_escalacao);

CREATE TABLE RESULTADO(
	id_partida INTEGER CONSTRAINT pk_resultado PRIMARY KEY,
	vencedor INTEGER,
	empate BOOLEAN,
	perdedor INTEGER,
	amarelos INTEGER,
	vermelhos INTEGER,
	CONSTRAINT fk_jogo FOREIGN KEY (id_partida) REFERENCES PARTIDA(id_partida)
);
