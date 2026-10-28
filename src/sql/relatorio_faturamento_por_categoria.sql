SELECT c.nome AS categoria
     , COUNT(a.id_aluguel) AS total_alugueis
     , SUM(a.valor_total) AS faturamento
     , ROUND(AVG(a.valor_total), 2) AS ticket_medio
  FROM aluguel a
 INNER JOIN veiculo v
    ON v.id_veiculo = a.id_veiculo
 INNER JOIN categoria c
    ON c.id_categoria = v.id_categoria
 WHERE a.status <> 'CANCELADO'
 GROUP BY c.nome
 ORDER BY faturamento DESC;
