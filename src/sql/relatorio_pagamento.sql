SELECT p.id_pagamento
     , p.id_aluguel
     , p.valor
     , p.data_pagamento
     , p.metodo
     , p.status
  FROM pagamento p
 INNER JOIN aluguel a
    ON p.id_aluguel = a.id_aluguel
 ORDER BY p.data_pagamento DESC;
