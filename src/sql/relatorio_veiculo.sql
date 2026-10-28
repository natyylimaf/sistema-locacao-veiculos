SELECT v.id_veiculo
     , v.placa
     , v.marca
     , v.modelo
     , v.ano
     , v.valor_diaria
     , ct.nome AS nome_categoria_veiculo
  FROM veiculo v
 INNER JOIN categoria ct
    ON v.id_categoria = ct.id_categoria
 ORDER BY v.ano DESC, v.marca;
