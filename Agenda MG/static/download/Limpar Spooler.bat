    echo off

    cls

    title Deletar trabalhos na Fila de Impressao e Reiniciar o Spooler de Impressao

 echo.

 echo Parando os servi�os do Spooler...
    net stop spooler

 echo Deletando documentos na Fila de Impress�o...
    cd %systemroot%\system32\spool\printers

 dir
    del /f/s *.shd
    del /f/s *.spl

 echo Reiniciando os servi�os do Spooler...
    net start spooler

 echo Fim do Processo...

 echo.

    pause
