    echo off

    cls

    title Deletar trabalhos na Fila de Impressao e Reiniciar o Spooler de Impressao

 echo.

 echo Parando os serviços do Spooler...
    net stop spooler

 echo Deletando documentos na Fila de Impressão...
    cd %systemroot%\system32\spool\printers

 dir
    del /f/s *.shd
    del /f/s *.spl

 echo Reiniciando os serviços do Spooler...
    net start spooler

 echo Fim do Processo...

 echo.

    pause
