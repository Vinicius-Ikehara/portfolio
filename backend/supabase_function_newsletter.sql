-- Função PostgreSQL para buscar newsletter com imagens dos artistas
-- Execute este SQL no Supabase SQL Editor

-- Primeiro, remover a função se ela já existir
DROP FUNCTION IF EXISTS get_newsletter_with_images(DATE);

-- Criar a função
CREATE OR REPLACE FUNCTION get_newsletter_with_images(data_ranking DATE)
RETURNS TABLE (
  id INTEGER,
  artista TEXT,
  imagem_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY
  SELECT
    n.id,
    n.artista,
    m.imagem_url,
    n.created_at
  FROM newsletter n
  LEFT JOIN (
    SELECT DISTINCT ON (mu.artista)
      mu.artista,
      mu.imagem_url
    FROM rankings_diarios r
    JOIN musicas mu
      ON mu.id = r.musica_id
    WHERE r.data = data_ranking
      AND mu.imagem_url IS NOT NULL
    ORDER BY mu.artista, r.posicao ASC
  ) m ON m.artista = n.artista;
END;
$$;
