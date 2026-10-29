SELECT a.id_aluguel
     , c.nome AS nome_cliente
     , l.nome AS nome_locadora
     , v.marca
     , v.modelo
     , f.nome AS nome_funcionario
     , a.data_retirada
     , a.data_devolucao_prevista
     , a.data_devolucao_real
     , a.valor_total
     , a.status
  FROM aluguel a
 INNER JOIN cliente c
    ON a.id_cliente = c.id_cliente
 INNER JOIN locadora l
    ON a.id_locadora = l.id_locadora
 INNER JOIN veiculo v
    ON a.id_veiculo = v.id_veiculo
 INNER JOIN funcionario f
    ON a.id_funcionario = f.id_funcionario
 ORDER BY a.id_aluguel;
