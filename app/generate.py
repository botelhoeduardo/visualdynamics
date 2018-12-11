import os, errno
from datetime import datetime
from .config import Config

def generate(
    selecao_arquivo, campo_forca, modelo_agua, tipo_caixa,
    distancia_caixa, neutralizar_sistema, double, ignore,
    current_user):

    arquivo = os.path.basename(selecao_arquivo)
    (nome_arquivo, extensao) = arquivo.split('.')

    #pasta = os.path.dirname(selecao_arquivo)
    pasta = Config.UPLOAD_FOLDER + current_user.username + '/' + nome_arquivo + '/'
    try:
        os.makedirs(pasta + '/run/logs/') #criando todas as pastas
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    arquivo_gro = nome_arquivo + '.gro'
    arquivo_top = nome_arquivo + '.top'
    arquivo_box = nome_arquivo + '_box'
    arquivo_ionizado = nome_arquivo + '_charged'
    
    # a@a.com/
    CompleteFileName = "{} - {}-{}-{} [{}:{}:{}].txt".format(
            nome_arquivo, datetime.now().year, datetime.now().month,
            datetime.now().day, datetime.now().hour,
            datetime.now().minute, datetime.now().second
            )
    
    # trabalhando parametros
    comandos = open(pasta + CompleteFileName, "w")

    #print("cd "+pasta)
    #comandos.writelines("cd "+pasta+"\n\n\n\n")

    os.chdir(pasta)          ## Estgabelece o diretório de trabalho

    # Montagem do comando gmx pdb2gmx com parametros para geracao da topologia a partir da estrutura PDB selecionada, campos de forca e modelo de agua
    gmx = '/usr/local/gromacs/bin/gmx_d' if double else '/usr/local/gromacs/bin/gmx'
    comando = 'pdb2gmx'
    parametro1 = '-f'
    parametro2 = arquivo
    parametro3 = '-o'
    parametro4 = arquivo_gro
    parametro5 = '-p'
    parametro6 = arquivo_top
    parametro7 = '-ff'
    parametro8 = campo_forca
    parametro9 = '-water'
    parametro10 = modelo_agua
    parametro11 = '-ignh -missing' #para ignorar hidrogenios e atomos faltando
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 \
    + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' \
    + parametro7 + ' ' + parametro8 + ' ' + parametro9 + ' ' + parametro10 \
    + (' ' + parametro11 if ignore else ''))
    comandos.write('\n\n')
    #print(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' + parametro7 + ' ' + parametro8 + ' ' + parametro9 + ' ' + parametro10)
    #r=subprocess.Popen([gmx, comando, parametro1, parametro2, parametro3, parametro4, parametro5, parametro6, parametro7, parametro8,parametro9, parametro10])


    # Montagem do comando gmx editconf com parametros para geracao da caixa
    # gmx editconf -f pfOxoacyl.gro -c -d 1.0 -bt cubic -o
    comando = 'editconf'
    parametro1 = '-f'
    parametro2 = arquivo_gro
    parametro3 = '-c'
    parametro4 = '-d'
    parametro5 = str(distancia_caixa)
    parametro6 = '-bt'
    parametro7 = tipo_caixa
    parametro8 = '-o'
    #print(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' +parametro5 + ' ' + parametro6 + ' ' + parametro7 + ' ' + parametro8)
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' +parametro5 + ' ' + parametro6 + ' ' + parametro7 + ' ' + parametro8)
    comandos.write('\n\n')
    #s=subprocess.Popen([gmx, comando, parametro1, parametro2, parametro3, parametro4, parametro5, parametro6, parametro7, parametro8])


    # Montagem do comando gmx solvate  com parametros para solvatacao da proteina
    # gmx solvate -cp out.gro -cs -p pfOxoacyl.top -o pfOxoacyl_box
    comando = 'solvate'
    parametro1 = '-cp'
    parametro2 = 'out.gro'          ## esse arquivo ficou padronizado e estático, é a saída do comando editconf
    parametro3 = '-cs'
    parametro4 = '-p'
    parametro5 =  arquivo_top
    parametro6 = '-o'
    parametro7 = arquivo_box
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' + parametro7)
    comandos.write('\n\n')
    #print(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' + parametro7)
    #t=subprocess.Popen([gmx, comando, parametro1, parametro2, parametro3, parametro4, parametro5, parametro6, parametro7])

    # Montagem do comando gmx grompp para precompilar e ver se o sistema esta carregado
    # grompp -f PME_em.mdp -c pfHGPRT_box.gro -p pfHGPRT.top -o pfHGPRT_charged
    comando = 'grompp'
    parametro1 = '-f'
    parametro2 = 'ions.mdp'        ## este arquivo ficará estático por hora.
    parametro3 = '-c'
    parametro4 = arquivo_box+'.gro'
    parametro5 = '-p'
    parametro6 = arquivo_top
    parametro7 ='-o'
    parametro8 = arquivo_ionizado
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' + parametro7 + ' ' + parametro8)
    comandos.write('\n\n')
    #print(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' + parametro7 + ' ' + parametro8)
    #u=subprocess.check_output([gmx, comando, parametro1, parametro2, parametro3, parametro4, parametro5, parametro6, parametro7,parametro8])

    if neutralizar_sistema: # se for True
    # Montagem do comando gmx genion para neutralizar o sistema
    # gmx genion -s pfOxoacyl_apo_charged.tpr -o pfOxoacyl_apo_charged -p pfOxoacyl_apo.top -neutral
        resposta = 'echo \"SOL\"'
        pipe = '|'
        comando = 'genion'
        parametro1 = '-s'
        parametro2 = arquivo_ionizado+'.tpr'
        parametro3 = '-o'
        parametro4 = arquivo_ionizado
        parametro5 = '-p'
        parametro6 = arquivo_top
        parametro7 = '-neutral'
        comandos.writelines(resposta + ' ' + pipe + ' ' + gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6+ ' ' + parametro7)
        #comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6+ ' ' + parametro7)
        comandos.write('\n\n')
        #print(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6+ ' ' + parametro7)
        #x = subprocess.Popen([gmx, comando, parametro1, parametro2, parametro3, parametro4, parametro5, parametro6]) ### Esse comando foi substituido pelo abaixo
        #ion = pexpect.spawnu(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6+ ' ' + parametro7)
        #ion.logfile = sys.stdout
        #time.sleep(5)
        #ion.expect(":")
        #ion.sendline("13" + "\r" )

        # pyatspi.Registry.generateKeyboardEvent(10, None, pyatspi.KEY_PRESSRELEASE)  ### Esses comandos foram uma tentativa de simular o pressionamento de teclas mas a opção acima se mostrou mais eficiente
        # pyatspi.Registry.generateKeyboardEvent(10, None, pyatspi.KEY_PRESSRELEASE)
        # pyatspi.Registry.generateKeyboardEvent(36, None, pyatspi.KEY_PRESSRELEASE)
        # Montagem do comando gmx grompp para precompilar e ver se o sistema esta carregado
        # grompp -f PME_em.mdp -c pfHGPRT_box.gro -p pfHGPRT.top -o pfHGPRT_charged

        # Montagem do comando gmx grompp para repetir a pre-compilacao caso seja selecionada a opcao de neutralizar o sistema
        # grompp -f PME_em.mdp -c pfHGPRT_box.gro -p pfHGPRT.top -o pfHGPRT_charged
        comando = 'grompp'
        parametro1 = '-f'
        parametro2 = 'PME_em.mdp'  ## este arquivo ficará estático por hora.
        parametro3 = '-c'
        parametro4 = arquivo_ionizado + '.gro'
        parametro5 = '-p'
        parametro6 = arquivo_top
        parametro7 = '-o'
        parametro8 = arquivo_ionizado
        comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' + parametro7 + ' ' + parametro8)
        comandos.write('\n\n')
        #print(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' + parametro7 + ' ' + parametro8)
        # t=subprocess.check_output([gmx, comando, parametro1, parametro2, parametro3, parametro4, parametro5, parametro6, parametro7,parametro8])

    # Montagem do comando gmx mdrun para executar a dinamica de minimizacao
    # #mdrun -v -s pfHGPRT_charged.tpr -deffnm pfHGPRT_sd_em
    arquivo_minimizado = nome_arquivo+'_sd_em'
    comando = 'mdrun'
    parametro1 = '-v'
    parametro2 = '-s'
    parametro3 =  arquivo_ionizado+'.tpr'
    parametro4 = '-deffnm'
    parametro5 = arquivo_minimizado
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5)
    comandos.write('\n\n')
    #print(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5)
    # u=subprocess.check_output([gmx, comando, parametro1, parametro2, parametro3, parametro4, parametro5])

    # Montagem do comando gmx grompp para precompilar a dinamica de minimizacao cg
    # grompp -f PME_cg_em.mdp -c pfHGPRT_sd_em.gro -p pfHGPRT.top -o pfHGPRT_cg_em
    comando = 'grompp'
    parametro1 = '-f'
    parametro2 = 'PME_cg_em.mdp'
    parametro3 = '-c'
    parametro4 = nome_arquivo+'_sd_em.gro'
    parametro5 = '-p'
    parametro6 = arquivo_top
    parametro7 = '-o'
    parametro8 = nome_arquivo+'_cg_em'
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5+ ' ' + parametro6+ ' ' + parametro7+ ' ' + parametro8)
    comandos.write('\n\n')
    #print(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5+ ' ' + parametro6+ ' ' + parametro7+ ' ' + parametro8)
    # v=subprocess.check_output([gmx, comando, parametro1, parametro2, parametro3, parametro4, parametro5, parametro6, parametro7, parametro8])

    # Montagem do comando gmx mdrun para executar a dinamica de minimizacao cg
    # mdrun -v -s pfHGPRT_cg_em.tpr -deffnm pfHGPRT_cg_em
    arquivo_minimizado_cg = nome_arquivo + '_cg_em'
    comando = 'mdrun'
    parametro1 = '-v'
    parametro2 = '-s'
    parametro3 = arquivo_minimizado_cg+'.tpr'
    parametro4 = '-deffnm'
    parametro5 = arquivo_minimizado_cg
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5)
    comandos.write('\n\n')
    #print(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5)
    # u=subprocess.check_output([gmx, comando, parametro1, parametro2, parametro3, parametro4, parametro5])

    #Montagem do comando gmx grompp para precompilar a primeira etapa do equilibrio
    # grompp -f nvt.mdp -c MjTXII_cg_em.gro -r MjTXII_cg_em.gro -p MjTXII.top -o MjTXII_nvt.tpr
    comando = 'grompp'
    parametro1 = '-f'
    parametro2 = 'nvt.mdp'
    parametro3 = '-c'
    parametro4 = nome_arquivo + '_cg_em.gro'
    parametro5 = '-r'
    parametro6 = parametro4
    parametro7 = '-p'
    parametro8 = arquivo_top
    parametro9 = '-o'
    parametro10 = nome_arquivo + '_nvt.tpr'
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' \
    + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' + parametro7 + ' ' + parametro8 + ' ' + parametro9 + ' ' + parametro10)
    comandos.write('\n\n')

    #Montagem do comando gmx mdrun para executar a primeira etapa do equilibrio
    # mdrun -v -s MjTXII_nvt.tpr -deffnm MjTXII_nvt
    arquivo_nvt = nome_arquivo + '_nvt'
    comando = 'mdrun'
    parametro1 = '-v'
    parametro2 = '-s'
    parametro3 = arquivo_nvt + '.tpr'
    parametro4 = '-deffnm'
    parametro5 = arquivo_nvt
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5)
    comandos.write('\n\n')


    #Montagem do comando gmx grompp para precompilar a segunda etapa do equilibrio
    # grompp -f npt.mdp -c MjTXII_nvt.gro -r MjTXII_nvt.gro -p MjTXII.top -o MjTXII_npt.tpr
    comando = 'grompp'
    parametro1 = '-f'
    parametro2 = 'npt.mdp'
    parametro3 = '-c'
    parametro4 = nome_arquivo + '_nvt.gro'
    parametro5 = '-r'
    parametro6 = parametro4
    parametro7 = '-p'
    parametro8 = arquivo_top
    parametro9 = '-o'
    parametro10 = nome_arquivo + '_npt.tpr'
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' \
    + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' + parametro7 + ' ' + parametro8 + ' ' + parametro9 + ' ' + parametro10)
    comandos.write('\n\n')

    #Montagem do comando gmx mdrun para executar a segunda etapa do equilibrio
    # mdrun -v -s MjTXII_npt.tpr -deffnm MjTXII_npt
    arquivo_npt = nome_arquivo + '_npt'
    comando = 'mdrun'
    parametro1 = '-v'
    parametro2 = '-s'
    parametro3 = arquivo_npt + '.tpr'
    parametro4 = '-deffnm'
    parametro5 = arquivo_npt
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5)
    comandos.write('\n\n')

    # Montagem do comando gmx grompp para precompilar a dinamica de position restraints VERSÃO 2
    # grompp -f md_pr.mdp -c MjTXII_npt.gro -p MjTXII.top -o MjTXII_pr
    comando = 'grompp'
    parametro1 = '-f'
    parametro2 = 'md_pr.mdp'
    parametro3 = '-c'
    parametro4 = nome_arquivo + '_npt.gro'
    parametro5 = '-p'
    parametro6 = arquivo_top
    parametro7 = '-o'
    parametro8 = nome_arquivo + '_pr'
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' + parametro7 + ' ' + parametro8)
    comandos.write('\n\n')
    #print(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5 + ' ' + parametro6 + ' ' + parametro7 + ' ' + parametro8)
    # v=subprocess.check_output([gmx, comando, parametro1, parametro2, parametro3, parametro4, parametro5, parametro6, parametro7, parametro8])


    # Montagem do comando gmx mdrun para executar a dinamica de position restraints
    # mdrun -v -s MjTXII_pr.tpr -deffnm MjTXII_pr
    arquivo_pr = nome_arquivo + '_pr'
    comando = 'mdrun'
    parametro1 = '-v'
    parametro2 = '-s'
    parametro3 = arquivo_pr + '.tpr'
    parametro4 = '-deffnm'
    parametro5 = arquivo_pr
    comandos.writelines(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5)
    comandos.write('\n\n')
    #print(gmx + ' ' + comando + ' ' + parametro1 + ' ' + parametro2 + ' ' + parametro3 + ' ' + parametro4 + ' ' + parametro5)
    # u=subprocess.check_output([gmx, comando, parametro1, parametro2, parametro3, parametro4, parametro5])

    comandos.close()
    return CompleteFileName