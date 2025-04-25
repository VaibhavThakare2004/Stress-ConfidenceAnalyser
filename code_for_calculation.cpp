#include<bits/stdc++.h>
using namespace std;

int main(){
    vector<int>result;
    ifstream file("report.csv");
    string line;
    bool skip_header=true;
    while(getline(file,line)){
        if(skip_header){
            skip_header=false;
            continue;
        }
    
    stringstream ss(line);
    //stringstream is a class. "ss" is object. it allows us to read the line in the string form
    string cell;
    int col_index=0;
    int value1=0,value2=0;
    
    while(getline(ss,cell,',')){
        if(col_index==3)
        value1=stoi(cell);
        if(col_index==4)
        value2=stoi(cell);
        col_index++;
    }
    result.push_back(value1+value2);
    }
    file.close();

    ofstream rfile("Result.txt");
    for(int i=0;i<result.size();i++){
        rfile<<result[i]<<endl;
    }
    rfile.close();
    return 0;
}
