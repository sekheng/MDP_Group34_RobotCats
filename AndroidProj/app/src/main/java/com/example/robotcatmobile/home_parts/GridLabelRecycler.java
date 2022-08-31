package com.example.robotcatmobile.home_parts;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.robotcatmobile.R;

public class GridLabelRecycler extends RecyclerView.Adapter<GridLabelRecycler.ViewHolder> {
    boolean mIsColumns;

    public GridLabelRecycler(boolean isColumn) {
        mIsColumns = isColumn;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.grid_row_label, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        holder.mLabelTxt.setText(Integer.toString(position + 1));
    }

    @Override
    public int getItemCount() {
        return mIsColumns ? GridRecycler.COLUMNS : GridRecycler.ROWS;
    }

    class ViewHolder extends RecyclerView.ViewHolder {
        public TextView mLabelTxt;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            mLabelTxt = itemView.findViewById(R.id.grid_labelTxt);
        }
    }
}
