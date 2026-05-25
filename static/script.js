function mostrarMensagem(mensagem, sucesso = true) {

    const resultado = document.getElementById('resultado');

    resultado.innerHTML = mensagem;

    if (sucesso) {
        resultado.style.backgroundColor = '#c8f7c5';
        resultado.style.color = '#1b5e20';
    }
    else {
        resultado.style.backgroundColor = '#ffcdd2';
        resultado.style.color = '#b71c1c';
    }
}


async function criarBanco() {

    try {

        const resposta = await fetch('/criar-banco', {
            method: 'POST'
        });

        const dados = await resposta.json();

        mostrarMensagem(dados.mensagem, dados.sucesso);

    }
    catch (erro) {

        mostrarMensagem(
            'Erro ao conectar com o servidor.',
            false
        );

        console.log(erro);
    }
}


async function destruirBanco() {

    const confirmado = confirm('Tem certeza que deseja destruir o banco de dados? Esta ação não pode ser desfeita.');

    if (!confirmado) return;

    try {

        const resposta = await fetch('/destruir-banco', {
            method: 'POST'
        });

        const dados = await resposta.json();

        mostrarMensagem(dados.mensagem, dados.sucesso);

    }
    catch (erro) {

        mostrarMensagem(
            'Erro ao conectar com o servidor.',
            false
        );

        console.log(erro);
    }
}


async function cadastrarCliente() {

    try {

        const dados = {
            nome: document.getElementById('clienteNome').value,
            idade: document.getElementById('clienteIdade').value,
            sexo: document.getElementById('clienteSexo').value,
            data_nascimento: document.getElementById('clienteNascimento').value
        };

        const resposta = await fetch('/cadastrar-cliente', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        mostrarMensagem(
            resultado.mensagem,
            resultado.sucesso
        );
    }
    catch (erro) {

        mostrarMensagem(
            'Erro ao cadastrar cliente.',
            false
        );

        console.log(erro);
    }
}


async function cadastrarProduto() {

    try {

        const dados = {
            nome: document.getElementById('produtoNome').value,
            descricao: document.getElementById('produtoDescricao').value,
            estoque: document.getElementById('produtoEstoque').value,
            valor: document.getElementById('produtoValor').value,
            observacoes: document.getElementById('produtoObservacoes').value,
            id_vendedor: document.getElementById('produtoVendedor').value
        };

        const resposta = await fetch('/cadastrar-produto', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        mostrarMensagem(
            resultado.mensagem,
            resultado.sucesso
        );
    }
    catch (erro) {

        mostrarMensagem(
            'Erro ao cadastrar produto.',
            false
        );

        console.log(erro);
    }
}


async function carregarProdutos() {

    try {

        const resposta = await fetch('/produtos');
        const dados = await resposta.json();

        if (!dados.sucesso || dados.produtos.length === 0) {
            mostrarMensagem('Nenhum produto disponível em estoque.', false);
            return;
        }

        const lista = document.getElementById('listaProdutos');

        lista.innerHTML = '';

        dados.produtos.forEach(produto => {

            const div = document.createElement('div');

            div.className = 'item-venda';

            div.innerHTML = `
                <span>
                    <strong>${produto.nome}</strong> —
                    R$ ${parseFloat(produto.valor).toFixed(2)} |
                    Estoque: ${produto.quantidade_estoque}
                </span>
                <input
                    type="number"
                    min="0"
                    value="0"
                    id="qty-${produto.id}"
                    placeholder="Quantidade"
                    data-id="${produto.id}"
                    data-estoque="${produto.quantidade_estoque}"
                >
            `;

            lista.appendChild(div);
        });

    }
    catch (erro) {

        mostrarMensagem('Erro ao carregar produtos.', false);
        console.log(erro);
    }
}


async function realizarVenda() {

    try {

        const idCliente = document.getElementById('vendaIdCliente').value;
        const idTransportadora = document.getElementById('vendaIdTransportadora').value;
        const endereco = document.getElementById('vendaEndereco').value;
        const valorTransporte = document.getElementById('vendaValorTransporte').value;

        const inputs = document.querySelectorAll('#listaProdutos input[type="number"]');

        if (inputs.length === 0) {
            mostrarMensagem('Carregue os produtos antes de confirmar a venda.', false);
            return;
        }

        const itens = [];

        for (const input of inputs) {

            const quantidade = parseInt(input.value);
            const estoque = parseInt(input.dataset.estoque);

            if (quantidade > 0) {

                if (quantidade > estoque) {
                    mostrarMensagem(`Quantidade informada ultrapassa o estoque disponível (${estoque}).`, false);
                    return;
                }

                itens.push({
                    id_produto: parseInt(input.dataset.id),
                    quantidade: quantidade
                });
            }
        }

        if (itens.length === 0) {
            mostrarMensagem('Informe a quantidade de pelo menos um produto.', false);
            return;
        }

        const dados = {
            id_cliente: idCliente,
            id_transportadora: idTransportadora,
            endereco: endereco,
            valor_transporte: valorTransporte,
            itens: itens
        };

        const resposta = await fetch('/realizar-venda', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        mostrarMensagem(resultado.mensagem, resultado.sucesso);

        if (resultado.sucesso) {
            document.getElementById('listaProdutos').innerHTML = '';
        }
    }
    catch (erro) {

        mostrarMensagem(
            'Erro ao realizar venda.',
            false
        );

        console.log(erro);
    }
}


async function reajustarSalario() {

    try {

        const dados = {
            percentual: document.getElementById('reajustePercentual').value,
            id_cargo: document.getElementById('reajusteIdCargo').value
        };

        const resposta = await fetch('/reajuste', {

            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        mostrarMensagem(
            resultado.mensagem,
            resultado.sucesso
        );
    }
    catch (erro) {

        mostrarMensagem(
            'Erro ao aplicar reajuste.',
            false
        );

        console.log(erro);
    }
}


async function sortearCliente() {

    try {

        const resposta = await fetch('/sortear-cliente', {
            method: 'POST'
        });

        const dados = await resposta.json();

        mostrarMensagem(dados.mensagem, dados.sucesso);

    }
    catch (erro) {

        mostrarMensagem(
            'Erro ao realizar sorteio.',
            false
        );

        console.log(erro);
    }
}


async function verEstatisticas() {

    try {

        const resposta = await fetch('/estatisticas');

        const dados = await resposta.json();

        if (!dados.sucesso) {
            mostrarMensagem(dados.mensagem, false);
            return;
        }

        const m = dados.dados.produto_mais;
        const me = dados.dados.produto_menos;

        const html = `
            <h3 style="margin-top: 16px;"> Produto mais vendido</h3>
            <p><strong>Nome:</strong> ${m.nome}</p>
            <p><strong>Vendedor:</strong> ${m.vendedor}</p>
            <p><strong>Quantidade vendida:</strong> ${m.quantidade}</p>
            <p><strong>Valor total arrecadado:</strong> R$ ${m.total.toFixed(2)}</p>
            <p><strong>Mês de maior venda:</strong> ${m.mes_maior}</p>
            <p><strong>Mês de menor venda:</strong> ${m.mes_menor}</p>

            <hr style="margin: 16px 0;">

            <h3> Produto menos vendido</h3>
            <p><strong>Nome:</strong> ${me.nome}</p>
            <p><strong>Vendedor:</strong> ${me.vendedor}</p>
            <p><strong>Quantidade vendida:</strong> ${me.quantidade}</p>
            <p><strong>Valor total arrecadado:</strong> R$ ${me.total.toFixed(2)}</p>
            <p><strong>Mês de maior venda:</strong> ${me.mes_maior}</p>
            <p><strong>Mês de menor venda:</strong> ${me.mes_menor}</p>
        `;

        const div = document.getElementById('estatisticasResultado');

        div.innerHTML = html;
        div.style.marginTop = '16px';

    }
    catch (erro) {

        mostrarMensagem(
            'Erro ao buscar estatísticas.',
            false
        );

        console.log(erro);
    }
}