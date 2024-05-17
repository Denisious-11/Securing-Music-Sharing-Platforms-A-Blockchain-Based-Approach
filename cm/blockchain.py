import random
import sys
import base64

import json

from web3 import Web3
from solcx import compile_standard

import solcx
#solcx.install_solc()

compiled_sol = compile_standard({
     "language": "Solidity",
     "sources": {
         "phb.sol": {
             "content": '''
                 pragma solidity >=0.4.0 <0.8.16;
               

                contract PHB {

                    struct Artist
                    {            
                        int user_id;
                        string username;
                        string password;
                        string mobile;
                        string p_address;
                    }

                    Artist []arts;

                    function addArtist(int user_id,string memory username,string memory password,string memory mobile,string memory p_address) public
                    {
                        Artist memory e
                            =Artist(user_id,
                                    username,
                                    password,
                                    mobile,
                                    p_address);
                        arts.push(e);
                    }

                    function getArtist(int user_id) public view returns(
                            string memory,
                            string memory,
                            string memory,
                            string memory
                            )
                    {
                        uint i;
                        for(i=0;i<arts.length;i++)
                        {
                            Artist memory e
                                =arts[i];
                            
                            if(e.user_id==user_id)
                            {
                                return(e.username,
                                    e.password,
                                    e.mobile,
                                    e.p_address
                                   
                                   );
                            }
                        }
                        
                        
                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found"
                               );
                    }

                    function getArtistCount() public view returns(uint256)
                    {
                        return(arts.length);
                    }


                     struct User
                    {
       
                        int user_id;
                        string username;
                        string password;
                        string mobile;
                        string p_address;
                    }

                    User []uss;

                    function addUser(int user_id,string memory username,string memory password,string memory mobile,string memory p_address) public
                    {
                        User memory e
                            =User(user_id,
                                    username,
                                    password,
                                    mobile,
                                    p_address);
                        uss.push(e);
                    }


                    function getUser(int user_id) public view returns(
                            string memory,
                            string memory,
                            string memory,
                            string memory
                            )
                    {
                        uint i;
                        for(i=0;i<uss.length;i++)
                        {
                            User memory e
                                =uss[i];
                                 
                            
                            if(e.user_id==user_id)
                            {
                                return(e.username,
                                    e.password,
                                    e.mobile,
                                    e.p_address
                                   );
                            }
                        }
                        
                        
                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found");
                    }

                    function getUserCount() public view returns(uint256)
                    {
                        return(uss.length);
                    }


                    struct Music
                    {            
                        int m_id;
                        string title;
                        string author;
                        string date;
                        string time;
                        string hash_value;

                    }

                    Music []msc;

                    function addMusic(int m_id,string memory title, string memory author, string memory date,string memory time,string memory hash_value) public
                    {
                        Music memory e
                            =Music(m_id,
                                    title,
                                    author,
                                    date,
                                    time,
                                    hash_value);
                        msc.push(e);
                    }

                    function getMusic(int m_id) public view returns(
                           
                            string memory,
                            string memory,
                            string memory,
                            string memory,
                            string memory
                            )
                    {
                        uint i;
                        for(i=0;i<msc.length;i++)
                        {
                            Music memory e
                                =msc[i];
                            
                            if(e.m_id==m_id)
                            {
                                return(e.title,
                                    e.author,
                                    e.date,
                                    e.time,
                                    e.hash_value
                                   );
                            }
                        }
                        
                        
                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found"
                               );
                    }

                    function getMusicCount() public view returns(uint256)
                    {
                        return(msc.length);
                    }

                    struct Transaction
                    {
                        int t_id;
                        string title;
                        string sender_name;
                        string receiver_name;
                        string sender_p_address;
                        string receiver_p_address;
                        string amount;
                        string t_hash;
                    }
                    Transaction []transactions;

                    function addTransaction(int t_id,string memory title,string memory sender_name,string memory receiver_name,string memory sender_p_address,string memory receiver_p_address,string memory amount,string memory t_hash)public
                    {
                        Transaction memory t=Transaction(t_id,
                                                        title,
                                                        sender_name,
                                                        receiver_name,
                                                        sender_p_address,
                                                        receiver_p_address,
                                                        amount,
                                                        t_hash);
                        transactions.push(t);
                    }

                    function getTransaction(int t_id) public view returns(string memory,
                                                                            string memory,
                                                                            string memory,
                                                                            string memory,
                                                                            string memory,
                                                                            string memory,
                                                                            string memory)
                    {
                        uint j;
                        for(j=0;j<transactions.length;j++)
                        {
                            Transaction memory t=transactions[j];

                            if(t.t_id==t_id)
                            {
                                return(t.title,
                                        t.sender_name,
                                        t.receiver_name,
                                        t.sender_p_address,
                                        t.receiver_p_address,
                                        t.amount,
                                        t.t_hash);
                            }

                        }

                        return("Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found",
                                "Not Found");
                    }
                    function getTransactionsCount() public view returns(uint256)
                    {
                        return(transactions.length);
                    }


                }

               '''
         }
     },
     "settings":
         {
             "outputSelection": {
                 "*": {
                     "*": [
                         "metadata", "evm.bytecode"
                         , "evm.bytecode.sourceMap"
                     ]
                 }
             }
         }
 })


# web3.py instance



def verify_key(adr1,key,amount):
    try:
        ganache_url = "http://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        web3.eth.enable_unaudited_features()
        nonce = web3.eth.getTransactionCount(adr1)

        tx = {
            'nonce': nonce,
            'to': adr1,
            'value': web3.toWei(1, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei(amount, 'gwei'),
        }
        signed_tx = web3.eth.account.signTransaction(tx,key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        #print(web3.toHex(tx_hash))
        return "Yes"
    except Exception as e:
        print(e)  
        return "No"  



def create_contract():
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    # get bytecode
    bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    pb = w3.eth.contract(abi=abi, bytecode=bytecode)

    # # Submit the transaction that deploys the contract
    tx_hash = pb.constructor().transact()

    # # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print("tx_receipt.contractAddress: ",tx_receipt.contractAddress)
    f=open('contract_address.txt','w')
    f.write(tx_receipt.contractAddress)
    f.close()


def add_artist1(user_id,username,password,mobile,p_address):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))

	# get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    
    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    tx_hash = p1.functions.addArtist(user_id,username,password,mobile,p_address).transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    #print(tx_hash) 
    print(tx_receipt)

    

def get_artist(id1):
    id1=int(id1)
    p1=get_contract()
    store = p1.functions.getArtist(id1).call()
    print("store : ",store)
    return store

def get_artists():
    c=get_artist_count()
    c_names=['username','password','mobile','p_address']
    dict1={}
    for i in range(1,c+1):
        d=get_artist(i)
        dict2={}
        for j in range(len(c_names)):
            # print("j : ",j)
            # print(type(j))
            # if(j==4):
            #     print("entered")
            #     dict2[c_names[j]]=d[6]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print(dict1)
    return dict1        

def get_artist_count():
    p1=get_contract()
    store = p1.functions.getArtistCount().call()
    print(store)
    return int(store)


def get_user(id1):
    id1=int(id1)
    p1=get_contract()
    print(id1,'============')
    store = p1.functions.getUser(id1).call()
    print(store)
    return store

def get_users():
    c=get_user_count()
    c_names=['username','password','mobile','p_address']
    dict1={}
    for i in range(1,c+1):
        d=get_user(i)
        dict2={}
        for j in range(len(c_names)):
            # if j==5:
            #     dict2[c_names[j]]=d[7]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print(dict1)
    return dict1     


def get_user_count():
    p1=get_contract()
    store = p1.functions.getUserCount().call()
    print(store)
    return int(store)
    

def add_user1(user_id,username,password,mobile,p_address):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']
    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    # c=get_patient_count()+1
    tx_hash = p1.functions.addUser(user_id,username,password,mobile,p_address).transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print(tx_hash)

##############################
def add_music1(m_id,title,author,date,time,hash_value):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']
    p2 = w3.eth.contract(
        address=address,
        abi=abi
    )
    # c=get_patient_count()+1
    tx_hash = p2.functions.addMusic(m_id,title,author,date,time,hash_value).transact()
    #tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    print(tx_hash)


def get_music(id1):
    id1=int(id1)
    p1=get_contract()
    store = p1.functions.getMusic(id1).call()
    print("store : ",store)
    return store

def get_musics():
    c=get_music_count()
    c_names=['title','author','date','time','hash_value']
    dict1={}
    for i in range(1,c+1):
        d=get_music(i)
        dict2={}
        for j in range(len(c_names)):
            # print("j : ",j)
            # print(type(j))
            # if(j==4):
            #     print("entered")
            #     dict2[c_names[j]]=d[6]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print("File dictionary :::>",dict1)
    return dict1        

def get_music_count():
    p1=get_contract()
    store = p1.functions.getMusicCount().call()
    print(store)
    return int(store)


def get_contract():
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]#'0x3529A6ee990639C32bEe5F841a9649cdd0c6e0FD'
    print(type(w3.eth.accounts[0]))

	# get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    return p1



def verify_adr(s):
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected(),"##########")
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    adrs = w3.eth.accounts
    print(adrs)

    if s in adrs:
        return True
    else:
        return False    

def bverify_transaction(tx):
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected(),"##########")
    #w3 = Web3(Web3.EthereumTesterProvi
    x=w3.eth.getTransaction(tx)
    print(x)
    if x==None:
        print('Fake')
        return False
    else:
        print('Real')
        return True


###################
def add_transaction_to_table(get_id,title,username,author,sender_public_key,receiver_public_key,price,t_hash):
    f=open('contract_address.txt','r')
    address=f.read()
    f.close()
    blockchain_address = 'http://127.0.0.1:7545'
    # # Client instance to interact with the blockchain
    w3 = Web3(Web3.HTTPProvider(blockchain_address))

    print(w3.isConnected())
    #w3 = Web3(Web3.EthereumTesterProvider())

    # set pre-funded account as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(type(w3.eth.accounts[0]))

    # get bytecode
    # bytecode = compiled_sol['contracts']['phb.sol']['PHB']['evm']['bytecode']['object']

    # # get abi
    abi = json.loads(compiled_sol['contracts']['phb.sol']['PHB']['metadata'])['output']['abi']

    
    p1 = w3.eth.contract(
        address=address,
        abi=abi
    )
    tx_hash = p1.functions.addTransaction(get_id,title,username,author,sender_public_key,receiver_public_key,price,t_hash).transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

    #print(tx_hash) 
    print(tx_receipt)

    

def get_transact(id1):
    id1=int(id1)
    p1=get_contract()
    store = p1.functions.getTransaction(id1).call()
    print("store : ",store)
    return store

def get_transactions():
    c=get_transactionss_count()

    c_names=['title','sender_name','receiver_name','sender_p_address','receiver_p_address','amount','t_hash']
    dict1={}
    for i in range(1,c+1):
        d=get_transact(i)
        dict2={}
        for j in range(len(c_names)):
            # print("j : ",j)
            # print(type(j))
            # if(j==4):
            #     print("entered")
            #     dict2[c_names[j]]=d[6]
            # else:
            dict2[c_names[j]]=d[j]
        dict1[i]=dict2

    print(dict1)
    return dict1        

def get_transactionss_count():
    p1=get_contract()
    store = p1.functions.getTransactionsCount().call()
    print(store)
    return int(store)



def transfer(adr1,adr2,key,amount,sender_name,receiver_name,title):
    try:
        ganache_url = "http://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        web3.eth.enable_unaudited_features()
        nonce = web3.eth.getTransactionCount(adr1)

        tx = {
            'nonce': nonce,
            'to': adr2, #artist_address
            'value': web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei(amount, 'gwei'),
        }
        signed_tx = web3.eth.account.signTransaction(tx,key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(web3.toHex(tx_hash))
        generated_hash=web3.toHex(tx_hash)
        print("generated_hash : ",generated_hash)
        return generated_hash

    except Exception as e:
        print(e)  
        return False



if __name__=="__main__":
    pass

    # create_contract()




