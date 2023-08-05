# ConectividadeApp

## Version 1.1.2

### Know Issues

* **\#02** - Se nenhum "device" estiver cadastrado na base, o campo "Input the Device" ficará em branco e ao realizer uma requisição, um erro é retornado.

* **\#07** - Se um Ator for excluído do banco tendo feito alguma atividade anterior, o seu nome é excluído da lista de atores daquela atividade.

* **\#09** - Usuários têm a possibilidade de cadastrar Atividades para datas "futuras".

* **\#10** - Atualizar a página após cadastrar uma atividade com sucesso cria mais uma atividade idêntica.

### Fixed Issues

* **\#12** - Ao cadastrar um novo item no plugin, seja Atividades, seja Atores, etc., o registro de log fica duplucado no banco de dados.

## Version 1.1.1

### Know Issues

* **\#02** - Se nenhum "device" estiver cadastrado na base, o campo "Input the Device" ficará em branco e ao realizer uma requisição, um erro é retornado.

* **\#07** - Se um Ator for excluído do banco tendo feito alguma atividade anterior, o seu nome é excluído da lista de atores daquela atividade.

* **\#09** - Usuários têm a possibilidade de cadastrar Atividades para datas "futuras".

* **\#10** - Atualizar a página após cadastrar uma atividade com sucesso cria mais uma atividade idêntica.

### Fixed Issues

* **\#05** - Na página de adição de Atores, ao clicar no ícone de ajuda a seguinte mensagem de erro aparece:
    > Unable to load documentation, file not found: ...

* **\#06** - Ao tentar excluir um Ator clicando em "Delete", no canto superior direito da página de visualização individual do Ator
a seguinte mensagem de erro aparece:
    > First argument to get_object_or_404() must be a Model, Manager, or QuerySet, not 'NoneType'.

* **\#11** - As listas de Atividades exibem o Name atual do Device, em vez do Name do Old Device

## Version 1.1.0

### Know Issues

* **\#02** - Se nenhum "device" estiver cadastrado na base, o campo "Input the Device" ficará em branco e ao realizer uma requisição, um erro é retornado.

* **\#05** - Na página de adição de Atores, ao clicar no ícone de ajuda a seguinte mensagem de erro aparece:
    > Unable to load documentation, file not found: ...</del>

* **\#06** - Ao tentar excluir um Ator clicando em "Delete", no canto superior direito da página de visualização individual do Ator
a seguinte mensagem de erro aparece:
    > First argument to get_object_or_404() must be a Model, Manager, or QuerySet, not 'NoneType'.</del>

* **\#07** - Se um Ator for excluído do banco tendo feito alguma atividade anterior, o seu nome é excluído da lista de atores daquela atividade.

* **\#09** - Usuários têm a possibilidade de cadastrar Atividades para datas "futuras".

* **\#10** - Atualizar a página após cadastrar uma atividade com sucesso cria mais uma atividade idêntica.

* **\#11** - As listas de Atividades exibem o Name atual do Device, em vez do Name do Old Device

### Fixed Issues

* **\#01** - Campo "MAC" em OldDevice limitado a 12 caracteres retorna erro se ultrapassar esse limite.
    > value too long for type character varying(12)

## Version 0.1.0

### Know Issues

* **\#01** - Campo "MAC" em OldDevice limitado a 12 caracteres retorna erro se ultrapassar esse limite.
    > value too long for type character varying(12)

* **\#02** - Se nenhum "device" estiver cadastrado na base, o campo "Input the Device" ficará em branco e ao realizer uma requisição, um erro é retornado.

* **\#05** - Na página de adição de Atores, ao clicar no ícone de ajuda a seguinte mensagem de erro aparece:
    > Unable to load documentation, file not found: ...

* **\#06** - Ao tentar excluir um Ator clicando em "Delete", no canto superior direito da página de visualização individual do Ator
a seguinte mensagem de erro aparece:
    > First argument to get_object_or_404() must be a Model, Manager, or QuerySet, not 'NoneType'.

* **\#07** - Se um Ator for excluído do banco tendo feito alguma atividade anterior, o seu nome é excluido da lista de atores daquela atividade.

### Fixed Issues

* **\#03** - Ao adicionar uma atividade de forma bem sucedida, o usuário é redirecionardo para conectividadeapp/addactivity/ com uma página em branco.

* **\#08** - Na página /plugins/conectividadeapp/searchdevice/ o botão "Details", em qualquer dispositivo, não responde.

## Version 0.0.32

### Know Issues

* **\#01** - Campo "MAC" em OldDevice limitado a 12 caracteres retorna erro se ultrapassar esse limite.
    > value too long for type character varying(12)

* **\#02** - Se nenhum "device" estiver cadastrado na base, o campo "Input the Device" ficará em branco e ao realizer uma requisição, um erro é retornado.

* **\#03** - Ao adicionar uma atividade de forma bem sucedida, o usuário é redirecionardo para conectividadeapp/addactivity/ com uma página em branco.

* **\#05** - Na página de adição de Atores, ao clicar no ícone de ajuda a seguinte mensagem de erro aparece:
    > Unable to load documentation, file not found: ...

* **\#06** - Ao tentar excluir um Ator clicando em "Delete", no canto superior direito da página de visualização individual do Ator
a seguinte mensagem de erro aparece:
    > First argument to get_object_or_404() must be a Model, Manager, or QuerySet, not 'NoneType'.

* **\#07** - Se um Ator for excluido do banco tendo feito alguma atividade anterior, o seu nome é excluido da lista de atores daquela atividade.

* **\#08** - Na página /plugins/conectividadeapp/searchdevice/ o botão "Details", em qualquer dispositivo, não responde.

### Fixed Issues

* **\#04** - Ao adicionar um ator, a mensagem de erro abaixo listada aparece, porém mesmo assim o item é adicionado ao banco:

    > Reverse for 'list' not found. 'list' is not a valid view function or pattern name..

## Version 0.0.29

### Know Issues

* **\#01** - Campo "MAC" em OldDevice limitado a 12 caracteres retorna erro se ultrapassar esse limite.

* **\#02** - Se nenhum "device" estiver cadastrado na base, o campo "Input the Device" ficará em branco e ao realizer uma requisição, um erro é retornado.

* **\#03** - Ao adicionar uma atividade de forma bem sucedida, o usuário é redirecionardo para conectividadeapp/addactivity/ com uma página em branco.

* **\#04** - Ao adicionar um ator, a mensagem de erro abaixo listada aparece, porém mesmo assim o item é adicionado ao banco:

    > Reverse for 'list' not found. 'list' is not a valid view function or pattern name..

### Fixed Issues
