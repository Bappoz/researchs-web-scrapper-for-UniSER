import React, { useState } from "react";

interface FAQItem {
  question: string;
  answer: string;
}

interface TutorialStep {
  title: string;
  description: string;
  location: string;
  steps: string[];
}

const HelpPage: React.FC = () => {
  const [openFAQ, setOpenFAQ] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<"tutorial" | "faq">("tutorial");

  const tutorials: TutorialStep[] = [
    {
      title: "🔍 Como Pesquisar por Nome",
      description:
        "Busca um pesquisador pelo nome completo no Google Acadêmico",
      location: 'Dashboard → Aba "Nome do Pesquisador"',
      steps: [
        "Digite o nome completo do pesquisador no campo de busca",
        'Clique no botão "Buscar por Nome" (ícone de lupa)',
        "Uma nova aba abrirá com os resultados do Google Acadêmico",
        "Selecione manualmente o perfil correto do pesquisador",
        "Copie o link do perfil e use a busca por link (abaixo)",
      ],
    },
    {
      title: "🔗 Como Pesquisar por Link do Google Scholar",
      description:
        "Busca dados usando o link direto do perfil do Google Acadêmico",
      location: 'Dashboard → Aba "Link do Google Scholar"',
      steps: [
        "Cole o link do perfil do Google Scholar (ex: https://scholar.google.com/citations?user=...)",
        "Defina o número máximo de publicações a extrair (padrão: 10)",
        'Clique em "Buscar Publicações"',
        "O sistema vai extrair: nome, h-index, i10-index, citações totais, publicações",
        "Também busca dados do Lattes automaticamente (instituição, área, resumo)",
        "Os resultados aparecem abaixo em cards",
      ],
    },
    {
      title: "📊 Como Visualizar Resultados",
      description: "Entenda os dados exibidos após a busca",
      location: "Dashboard → Seção de Resultados",
      steps: [
        "Cards de Estatísticas: H-Index, I10-Index, Total de Citações",
        'Card "Dados do Lattes": instituição, área de atuação, resumo, link do currículo',
        "Lista de Publicações: título, autores, ano, citações, link",
        "Clique no link da publicação para abrir no Google Scholar",
        "Clique no link do Lattes para abrir o currículo completo",
      ],
    },
    {
      title: "📥 Como Exportar Dados",
      description: "Exporte todos os dados coletados para Excel",
      location: "Dashboard → Painel de Exportação (canto superior direito)",
      steps: [
        'Após realizar buscas, clique no botão "Gerar Excel Consolidado"',
        "O sistema gera um arquivo Excel com 2 abas:",
        '  • Aba "Pesquisadores": nome, instituição, h-index, métricas, dados Lattes',
        '  • Aba "Publicações": título, autores, ano, citações, journal, link',
        "O arquivo será baixado automaticamente",
        "Nome do arquivo: excel_consolidado_[data-hora].xlsx",
      ],
    },
    {
      title: "📚 Como Visualizar Histórico",
      description: "Acesse todos os pesquisadores já consultados",
      location: 'Menu Superior → Botão "Histórico de Pesquisadores"',
      steps: [
        'Clique em "Histórico de Pesquisadores" no topo da página',
        "Você verá uma tabela com todos os pesquisadores salvos",
        "Informações exibidas: nome, instituição, h-index, i10-index, citações",
        'Use o botão "Deletar" (ícone de lixeira) para remover um pesquisador',
        'Use "Limpar Histórico" para apagar todos os dados',
        'Clique em "Voltar ao Dashboard" para retornar',
      ],
    },
    {
      title: "🎨 Como Ativar Dark Mode",
      description: "Personalize a aparência do sistema",
      location: "Menu Superior → Botão de Sol/Lua",
      steps: [
        "Localize o ícone de sol/lua no canto superior direito",
        "Clique para alternar entre modo claro e escuro",
        "Sua preferência é salva automaticamente",
        "O tema se aplica a todas as páginas do sistema",
      ],
    },
  ];

  const faqs: FAQItem[] = [
    {
      question:
        "❌ Por que a busca por nome não retorna resultados automaticamente?",
      answer:
        "A busca por nome abre o Google Acadêmico em uma nova aba para você selecionar MANUALMENTE o perfil correto. Isso evita erros ao buscar pesquisadores com nomes similares. Após encontrar o perfil, copie o link e use a busca por link do Google Scholar.",
    },
    {
      question:
        '🔄 Os dados do Lattes aparecem como "NULL" ou "Instituição não especificada"',
      answer:
        "Isso pode acontecer por 3 motivos:\n1. O pesquisador não tem currículo Lattes cadastrado\n2. O nome extraído do Google Scholar é diferente do nome no Lattes\n3. O scraper não conseguiu acessar a Plataforma Lattes temporariamente (tente novamente em alguns minutos)\n\nSolução: Verifique se o pesquisador tem Lattes em buscatextual.cnpq.br",
    },
    {
      question: "📊 O que significam H-Index e I10-Index?",
      answer:
        "H-Index: Um pesquisador tem índice h quando possui h artigos com pelo menos h citações cada. Exemplo: h=10 significa 10 artigos com 10+ citações.\n\nI10-Index: Número total de publicações com pelo menos 10 citações. Indica produtividade acadêmica.",
    },
    {
      question: "🔗 Qual formato de link do Google Scholar é aceito?",
      answer:
        "O sistema aceita links no formato:\nhttps://scholar.google.com/citations?user=XXXXXXX\n\nOnde XXXXXXX é o ID único do pesquisador. Você encontra esse link ao acessar o perfil de qualquer pesquisador no Google Acadêmico.",
    },
    {
      question: "📥 O Excel não baixa ou aparece vazio",
      answer:
        "Causas possíveis:\n1. Nenhuma busca foi realizada ainda - faça ao menos uma busca antes de exportar\n2. Bloqueador de pop-ups ativo - permita downloads do site\n3. Erro no servidor - verifique o console do navegador (F12)\n\nSolução: Tente realizar uma nova busca e exportar novamente.",
    },
    {
      question: "🗑️ Como deletar apenas um pesquisador do histórico?",
      answer:
        'Vá em "Histórico de Pesquisadores" (botão no topo), localize o pesquisador na tabela e clique no ícone de lixeira 🗑️ na coluna "Ações". Isso remove apenas aquele pesquisador e suas publicações.',
    },
    {
      question:
        '⚠️ Erro: "Currículo disponível na Plataforma Lattes" aparece 4 vezes',
      answer:
        "Isso indica que o scraper encontrou o perfil no Lattes, mas não conseguiu extrair os dados específicos (instituição, área, resumo). Possíveis causas:\n1. Perfil do Lattes está incompleto\n2. Estrutura HTML do Lattes mudou\n3. Múltiplas requisições muito rápidas (aguarde 1-2 minutos)\n\nO link do Lattes ainda funciona - clique nele para ver o currículo completo.",
    },
    {
      question: "🔄 Posso buscar vários pesquisadores de uma vez?",
      answer:
        'Atualmente, o sistema busca um pesquisador por vez. Para múltiplos pesquisadores:\n1. Busque o primeiro pesquisador\n2. Aguarde os resultados aparecerem\n3. Busque o próximo pesquisador\n4. Todos ficam salvos no banco de dados\n5. Use "Gerar Excel Consolidado" para exportar todos de uma vez',
    },
    {
      question: "🌐 O site funciona offline?",
      answer:
        "NÃO. O sistema precisa de conexão com internet para:\n• Acessar Google Scholar e extrair dados\n• Buscar informações na Plataforma Lattes\n• Salvar dados no MongoDB (banco de dados)\n• Gerar arquivos Excel\n\nCertifique-se de ter conexão estável antes de usar.",
    },
    {
      question: "🎨 O Dark Mode não está salvando minha preferência",
      answer:
        "O Dark Mode usa localStorage do navegador. Se não está salvando:\n1. Verifique se o navegador permite cookies/localStorage\n2. Não está em modo anônimo/privado\n3. Limpe o cache do navegador e tente novamente\n4. Teste em outro navegador\n\nSe persistir, pode ser uma extensão bloqueando o localStorage.",
    },
    {
      question: "📱 O sistema funciona no celular?",
      answer:
        "SIM! O design é responsivo e funciona em dispositivos móveis. Porém, a experiência é melhor em desktop/laptop devido:\n• Tabelas grandes de publicações\n• Necessidade de copiar/colar links\n• Visualização de múltiplas abas\n\nRecomendamos usar no computador para melhor produtividade.",
    },
    {
      question: "⏱️ Quanto tempo leva uma busca?",
      answer:
        "Depende do número de publicações:\n• 10 publicações: ~5-10 segundos\n• 50 publicações: ~15-25 segundos\n• 100+ publicações: ~30-60 segundos\n\nA busca no Lattes adiciona 1-3 segundos extras. Aguarde o carregamento completo antes de fazer nova busca.",
    },
  ];

  const toggleFAQ = (index: number) => {
    setOpenFAQ(openFAQ === index ? null : index);
  };

  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200'>
      {/* Header */}
      <div className='bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6'>
          <div className='flex items-center justify-between'>
            <div>
              <h1 className='text-3xl font-bold text-gray-900 dark:text-white'>
                📖 Central de Ajuda
              </h1>
              <p className='mt-2 text-gray-600 dark:text-gray-400'>
                Aprenda a usar todas as funcionalidades do Web Scrapper
              </p>
            </div>
            <button
              onClick={() => (window.location.hash = "#/")}
              className='px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors'
            >
              ← Voltar ao Dashboard
            </button>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6'>
        <div className='border-b border-gray-200 dark:border-gray-700'>
          <nav className='-mb-px flex space-x-8'>
            <button
              onClick={() => setActiveTab("tutorial")}
              className={`${
                activeTab === "tutorial"
                  ? "border-blue-500 text-blue-600 dark:text-blue-400"
                  : "border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300"
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
            >
              📚 Tutoriais Passo a Passo
            </button>
            <button
              onClick={() => setActiveTab("faq")}
              className={`${
                activeTab === "faq"
                  ? "border-blue-500 text-blue-600 dark:text-blue-400"
                  : "border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300"
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
            >
              ❓ Dúvidas Frequentes (FAQ)
            </button>
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        {activeTab === "tutorial" ? (
          <div className='space-y-6'>
            {tutorials.map((tutorial, index) => (
              <div
                key={index}
                className='bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700'
              >
                <h3 className='text-xl font-bold text-gray-900 dark:text-white mb-2'>
                  {tutorial.title}
                </h3>
                <p className='text-gray-600 dark:text-gray-400 mb-3'>
                  {tutorial.description}
                </p>
                <div className='bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-500 p-3 mb-4'>
                  <p className='text-sm text-blue-800 dark:text-blue-300'>
                    <strong>📍 Localização:</strong> {tutorial.location}
                  </p>
                </div>
                <div>
                  <h4 className='font-semibold text-gray-900 dark:text-white mb-3'>
                    Passo a Passo:
                  </h4>
                  <ol className='list-decimal list-inside space-y-2'>
                    {tutorial.steps.map((step, stepIndex) => (
                      <li
                        key={stepIndex}
                        className='text-gray-700 dark:text-gray-300 leading-relaxed'
                      >
                        {step}
                      </li>
                    ))}
                  </ol>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className='space-y-4'>
            {faqs.map((faq, index) => (
              <div
                key={index}
                className='bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 overflow-hidden'
              >
                <button
                  onClick={() => toggleFAQ(index)}
                  className='w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors'
                >
                  <h3 className='text-lg font-semibold text-gray-900 dark:text-white pr-4'>
                    {faq.question}
                  </h3>
                  <svg
                    className={`w-5 h-5 text-gray-500 dark:text-gray-400 transform transition-transform ${
                      openFAQ === index ? "rotate-180" : ""
                    }`}
                    fill='none'
                    stroke='currentColor'
                    viewBox='0 0 24 24'
                  >
                    <path
                      strokeLinecap='round'
                      strokeLinejoin='round'
                      strokeWidth={2}
                      d='M19 9l-7 7-7-7'
                    />
                  </svg>
                </button>
                {openFAQ === index && (
                  <div className='px-6 py-4 bg-gray-50 dark:bg-gray-900/50 border-t border-gray-200 dark:border-gray-700'>
                    <div className='text-gray-700 dark:text-gray-300 whitespace-pre-line leading-relaxed'>
                      {faq.answer}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer Helper */}
      <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        <div className='bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-lg p-6 text-white'>
          <h3 className='text-xl font-bold mb-2'>💡 Dica Profissional</h3>
          <p className='text-blue-50'>
            Para melhor experiência, use a sequência:{" "}
            <strong>Busca por Nome</strong> → Copiar link do perfil →{" "}
            <strong>Busca por Link</strong> → Verificar resultados →{" "}
            <strong>Exportar Excel</strong>. Isso garante que você está
            capturando o pesquisador correto!
          </p>
        </div>
      </div>
    </div>
  );
};

export default HelpPage;
